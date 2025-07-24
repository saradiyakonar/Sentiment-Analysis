import pandas as pd
import string
import nltk
import textstat
import re
import os
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')

with open('positive-words.txt', 'r', encoding='utf-8') as f:
    positive_words = set(word.strip().lower() for word in f if word.strip() and not word.startswith(';'))

with open('negative-words.txt', 'r', encoding='latin-1') as f:
    negative_words = set(word.strip().lower() for word in f if word.strip() and not word.startswith(';'))

stopword_files = [
    'StopWords_Auditor.txt',
    'StopWords_Currencies.txt',
    'StopWords_DatesandNumbers.txt',
    'StopWords_Generic.txt',
    'StopWords_GenericLong.txt',
    'StopWords_Geographic.txt',
    'StopWords_Names.txt',
]

custom_stopwords = set()
for file in stopword_files:
    with open(file, 'r', encoding='latin-1') as f:
        custom_stopwords.update(word.strip().lower() for word in f if word.strip())


def clean_and_score_positive(text):
    words = str(text).lower().translate(str.maketrans('', '', string.punctuation)).split()
    filtered = [w for w in words if w not in custom_stopwords]
    return sum(1 for word in filtered if word in positive_words)

def clean_and_score_negative(text):
    words = str(text).lower().translate(str.maketrans('', '', string.punctuation)).split()
    filtered = [w for w in words if w not in custom_stopwords]
    return sum(1 for word in filtered if word in negative_words)

def clean_words_count(text):
    words = str(text).lower().translate(str.maketrans('', '', string.punctuation)).split()
    filtered = [w for w in words if w not in custom_stopwords]
    return len(filtered)

def count_words(text):
    text = str(text)
    return pd.Series({
        'word_count': len(word_tokenize(text)),
        'sent_count': len(sent_tokenize(text))
    })

def count_complex_words(text):
    words = str(text).split()
    return len([word for word in words if textstat.syllable_count(word) >= 2])

def syllables_per_word(text):
    words = str(text).split()
    total_syllables = sum(textstat.syllable_count(word) for word in words)
    return total_syllables / (len(words) + 1e-6)

def count_personal_pronouns(text):
    return len(re.findall(r'\b(I|we|my|ours|us|me|mine|our|you|your|yours)\b', str(text), re.IGNORECASE))

def average_word_length(text):
    words = str(text).translate(str.maketrans('', '', string.punctuation)).split()
    return sum(len(word) for word in words) / (len(words) + 1e-6)


mapping_df = pd.read_csv("mapping.csv")  

results = []

for i in range(1, 148):
    article_path = f"selenium_articles/article{i}.csv"
    if not os.path.exists(article_path):
        continue
    
    try:
        df = pd.read_csv(article_path)
        if 'content' not in df.columns or 'url' not in df.columns:
            print(f"Missing 'content' or 'url' column in article{i}.csv, skipping.")
            continue
        
        content = str(df.iloc[0]['content'])
        url = df.iloc[0]['url']
        
        url_row = mapping_df[mapping_df['URL'] == url]
        
        if url_row.empty:
            print(f"No URL_ID found for URL {url} in mapping.csv, skipping article{i}.csv.")
            continue
        
        url_id = url_row['URL_ID'].values[0]

        pos_score = clean_and_score_positive(content)
        neg_score = clean_and_score_negative(content)
        cleaned_wc = clean_words_count(content)
        polarity = (pos_score - neg_score) / ((pos_score + neg_score) + 1e-6)
        subjectivity = (pos_score + neg_score) / (cleaned_wc + 1e-6)

        word_info = count_words(content)
        avg_sent_len= word_info['word_count'] / (word_info['sent_count'] + 1e-6)

        complex_words = count_complex_words(content)
        perc_complex = complex_words / (word_info['word_count'] + 1e-6)
        fog_index = 0.4 * (avg_sent_len + perc_complex)

        syllable_per_word = syllables_per_word(content)
        personal_pronouns = count_personal_pronouns(content)
        avg_word_len = average_word_length(content)

        results.append([
            url_id, url, pos_score, neg_score, polarity, subjectivity,
            avg_sent_len, perc_complex, fog_index, avg_sent_len,
            complex_words, word_info['word_count'], syllable_per_word,
            personal_pronouns, avg_word_len
        ])

    except Exception as e:
        print(f"Error processing article{i}: {e}")

columns = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
    'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH', 'PERCENTAGE COMPLEX WORDS',
    'FOG INDEX', ' AVG NUMBER OF WORDS', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]

final_df = pd.DataFrame(results, columns=columns)
final_df.to_excel('Output Data.xlsx', index=False)
print("Data written to Output Data.xlsx successfully.")

import os

# Adjust this to the list of your actual file paths
stopword_files = [
    'StopWords_Auditor.txt',
    'StopWords_Currencies.txt',
    'StopWords_DatesandNumbers.txt',
    'StopWords_Generic.txt',
    'StopWords_GenericLong.txt',
    'StopWords_Geographic.txt',
    'StopWords_Names.txt',
]

# Combine stopwords into a set
custom_stopwords = set()
for file in stopword_files:
  with open(file, 'r', encoding='latin-1') as f:
    custom_stopwords.update(word.strip().lower() for word in f if word.strip())


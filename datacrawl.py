import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

urls = [
'https://insights.blackcoffer.com/ai-and-ml-based-youtube-analytics-and-content-creation-tool-for-optimizing-subscriber-engagement-and-content-strategy/',
'https://insights.blackcoffer.com/enhancing-front-end-features-and-functionality-for-improved-user-experience-and-dashboard-accuracy-in-partner-hospital-application/',
'https://insights.blackcoffer.com/roas-dashboard-for-campaign-wise-google-ads-budget-tracking-using-google-ads-ap/',
'https://insights.blackcoffer.com/efficient-processing-and-analysis-of-financial-data-from-pdf-files-addressing-formatting-inconsistencies-and-ensuring-data-integrity-for-a-toyota-dealership-management-firm/',
'https://insights.blackcoffer.com/development-of-ea-robot-for-automated-trading/',
'https://insights.blackcoffer.com/ai-and-ml-based-youtube-analytics-and-content-creation-tool-for-optimizing-subscriber-engagement-and-content-strategy/',
'https://insights.blackcoffer.com/enhancing-front-end-features-and-functionality-for-improved-user-experience-and-dashboard-accuracy-in-partner-hospital-application/',
'https://insights.blackcoffer.com/roas-dashboard-for-campaign-wise-google-ads-budget-tracking-using-google-ads-ap/',
'https://insights.blackcoffer.com/efficient-processing-and-analysis-of-financial-data-from-pdf-files-addressing-formatting-inconsistencies-and-ensuring-data-integrity-for-a-toyota-dealership-management-firm/',
'https://insights.blackcoffer.com/transforming-and-managing-a-large-scale-sql-pedigree-database-to-neo4j-graph-db/',
'https://insights.blackcoffer.com/enhancing-model-accuracy-from-58-to-over-90-strategies-for-improving-predictive-performance/',
'https://insights.blackcoffer.com/securing-sensitive-financial-data-with-privacy-preserving-machine-learning-for-predictive-analytics/',
'https://insights.blackcoffer.com/enhancing-data-collection-for-research-institutions-addressing-survey-fatigue-and-incorporating-verbal-communication-for-richer-insights/',
'https://insights.blackcoffer.com/analyzing-the-impact-of-positive-emotions-and-pandemic-severity-on-mental-health-and-resilience-among-entrepreneurs-insights-and-predictive-modeling/',
'https://insights.blackcoffer.com/dynamic-brand-centric-dashboard-for-automotive-dealerships-pdf-to-financial-insights-with-flask-react-architecture-and-aws-cloud-hosting/',
'https://insights.blackcoffer.com/cloud-based-data-modeling-and-analysis-platform-with-drag-and-drop-interface-and-openai-api-integration-for-simulation-insights/',
'https://insights.blackcoffer.com/voter-profile-analysis-and-search-application-for-targeted-campaign-engagement-using-government-voter-data/',
'https://insights.blackcoffer.com/bert-based-classification-of-individuals-and-organizations-into-two-categories-using-natural-language-processing/',
'https://insights.blackcoffer.com/comprehensive-analysis-of-solana-and-ethereum-contributors-using-github-api-with-comparative-study-of-1000-random-github-profiles/',
'https://insights.blackcoffer.com/powerbi-rest-api-fetching-dataflow-and-refresh-schedules-with-semantic-models/',
'https://insights.blackcoffer.com/automated-job-data-import-and-management-solution-for-enhanced-efficiency/',
'https://insights.blackcoffer.com/data-analytics-and-optimization-solution-for-enhancing-renewable-energy-efficiency/',
'https://insights.blackcoffer.com/time-series-analysis-and-trend-forecasting-solution-for-predicting-news-trends/',
'https://insights.blackcoffer.com/advanced-data-visualization-solutions-for-monitoring-key-business-metrics-with-integrated-interactive-dashboards/',
'https://insights.blackcoffer.com/advanced-patient-data-analysis-solution-for-trend-identification-and-improved-healthcare-outcome/',
'https://insights.blackcoffer.com/anomaly-detection-and-analysis-for-enhanced-data-integrity-and-user-experience-on-bright-datas-website/',
'https://insights.blackcoffer.com/building-custom-tflite-models-and-benchmarking-on-voxl2-chips/',
'https://insights.blackcoffer.com/sports-prediction-model-for-multiple-sports-leagues/',
'https://insights.blackcoffer.com/efficient-coach-allocation-system-for-sports-coaching-organization/',
'https://insights.blackcoffer.com/data-studio-dashboard-with-a-data-pipeline-tool-synced-with-podio-using-custom-webhooks-and-google-cloud-function-2/',
'https://insights.blackcoffer.com/ai-driven-backend-for-audio-to-text-conversion-and-analytical-assessment-in-pharmaceutical-practice/',
'https://insights.blackcoffer.com/cloud-based-web-application-for-financial-data-processing-and-visualization-of-sp-500-metrics/',
'https://insights.blackcoffer.com/department-wise-kpi-tracking-dashboard-with-technician-performance-analysis-for-atoz-dependable-service/',
'https://insights.blackcoffer.com/steps-to-convert-a-node-js-api-to-python-for-aws-lambda-deployment/',
'https://insights.blackcoffer.com/building-an-analytics-dashboard-with-a-pdf-parsing-pipeline-for-data-extraction/',
'https://insights.blackcoffer.com/building-a-real-time-log-file-visualization-dashboard-in-kibana/',
'https://insights.blackcoffer.com/analyzing-the-impact-of-female-ceo-appointments-on-company-stock-prices/',
'https://insights.blackcoffer.com/ai-chatbot-using-llm-langchain-llama/',
'https://insights.blackcoffer.com/healthcare-ai-chatbot-using-llama-llm-langchain/',
'https://insights.blackcoffer.com/ai-bot-audio-to-audio/',
'https://insights.blackcoffer.com/recommendation-engine-for-insurance-sector-to-expand-business-in-the-rural-area/',
'https://insights.blackcoffer.com/data-from-crm-via-zapier-to-google-sheets-dynamic-to-powerbi/',
'https://insights.blackcoffer.com/data-warehouse-to-google-data-studio-looker-dashboard/',
'https://insights.blackcoffer.com/crm-monday-com-via-zapier-to-power-bi-dashboard/',
'https://insights.blackcoffer.com/monday-com-to-kpi-dashboard-to-manage-view-and-generate-insights-from-the-crm-data/',
'https://insights.blackcoffer.com/data-management-for-a-political-saas-application/',
'https://insights.blackcoffer.com/google-lsa-ads-google-local-service-ads-etl-tools-and-dashboards/',
'https://insights.blackcoffer.com/ad-networks-marketing-campaign-data-dashboard-in-looker-google-data-studio/',
'https://insights.blackcoffer.com/analytical-solution-for-a-tech-firm/',
'https://insights.blackcoffer.com/ai-solution-for-a-technology-information-and-internet-firm/',
'https://insights.blackcoffer.com/ai-and-nlp-based-solutions-to-automate-data-discovery-for-venture-capital-and-private-equity-principals/',
'https://insights.blackcoffer.com/an-etl-solution-for-an-internet-publishing-firm/',
'https://insights.blackcoffer.com/ai-based-algorithmic-trading-bot-for-forex/',
'https://insights.blackcoffer.com/equity-waterfalls-model-based-saas-application-for-real-estate-sector/',
'https://insights.blackcoffer.com/ai-solutions-for-foreign-exchange-an-automated-algo-trading-tool/',
'https://insights.blackcoffer.com/ai-agent-development-and-deployment-in-jina-ai/',
'https://insights.blackcoffer.com/golden-record-a-knowledge-graph-database-approach-to-unfold-discovery-using-neo4j/',
'https://insights.blackcoffer.com/advanced-ai-for-trading-automation/',
'https://insights.blackcoffer.com/create-a-knowledge-graph-to-provide-real-time-analytics-recommendations-and-a-single-source-of-truth/',
'https://insights.blackcoffer.com/advanced-ai-for-thermal-person-detection/',
'https://insights.blackcoffer.com/advanced-ai-for-road-cam-threat-detection/',
'https://insights.blackcoffer.com/advanced-ai-for-pedestrian-crossing-safety/',
'https://insights.blackcoffer.com/handgun-detection-using-yolo/',
'https://insights.blackcoffer.com/using-graph-technology-to-create-single-customer-view/',
'https://insights.blackcoffer.com/car-detection-in-satellite-images/',
'https://insights.blackcoffer.com/building-a-physics-informed-neural-network-for-circuit-evaluation/',
'https://insights.blackcoffer.com/connecting-mongodb-database-to-power-bi-dashboard-dashboard-automation/',
'https://insights.blackcoffer.com/data-transformation/',
'https://insights.blackcoffer.com/e-commerce-store-analysis-purchase-behavior-ad-spend-conversion-traffic-etc/',
'https://insights.blackcoffer.com/kpi-dashboard-for-accountants/',
'https://insights.blackcoffer.com/return-on-advertising-spend-dashboard-marketing-automation-and-analytics-using-etl-and-dashboard/',
'https://insights.blackcoffer.com/ranking-customer-behaviours-for-business-strategy/',
'https://insights.blackcoffer.com/algorithmic-trading-for-multiple-commodities-markets-like-forex-metals-energy-etc/',
'https://insights.blackcoffer.com/trading-bot-for-forex/',
'https://insights.blackcoffer.com/python-model-for-the-analysis-of-sector-specific-stock-etfs-for-investment-purposes%ef%bf%bc/',
'https://insights.blackcoffer.com/medical-classification/',
'https://insights.blackcoffer.com/design-develop-bert-question-answering-model-explanations-with-visualization/',
'https://insights.blackcoffer.com/design-and-develop-solution-to-anomaly-detection-classification-problems/',
'https://insights.blackcoffer.com/an-etl-solution-for-currency-data-to-google-big-query/',
'https://insights.blackcoffer.com/etl-and-mlops-infrastructure-for-blockchain-analytics/',
'https://insights.blackcoffer.com/an-agent-based-model-of-a-virtual-power-plant-vpp/',
'https://insights.blackcoffer.com/transform-api-into-sdk-library-and-widget/',
'https://insights.blackcoffer.com/integration-of-a-product-to-a-cloud-based-crm-platform/',
'https://insights.blackcoffer.com/a-web-based-dashboard-for-the-filtered-data-retrieval-of-land-records/',
'https://insights.blackcoffer.com/integration-of-video-conferencing-data-to-the-existing-web-app/',
'https://insights.blackcoffer.com/design-develop-an-app-in-retool-which-shows-the-progress-of-the-added-video/',
'https://insights.blackcoffer.com/auvik-connectwise-integration-in-grafana/',
'https://insights.blackcoffer.com/data-integration-and-big-data-performance-using-elk-stack/',
'https://insights.blackcoffer.com/web-data-connector/',
'https://insights.blackcoffer.com/an-app-for-updating-the-email-id-of-the-user-and-stripe-refund-tool-using-retool/',
'https://insights.blackcoffer.com/an-ai-ml-based-web-application-that-detects-the-correctness-of-text-in-a-given-video/',
'https://insights.blackcoffer.com/website-tracking-and-insights-using-google-analytics-google-tag-manager/',
'https://insights.blackcoffer.com/dashboard-to-track-the-analytics-of-the-website-using-google-analytics-and-google-tag-manager/',
'https://insights.blackcoffer.com/power-bi-dashboard-on-operations-transactions-and-marketing-embedding-the-dashboard-to-web-app/',
'https://insights.blackcoffer.com/nft-data-automation-looksrare-and-etl-tool/',
'https://insights.blackcoffer.com/optimize-the-data-scraper-program-to-easily-accommodate-large-files-and-solve-oom-errors/',
'https://insights.blackcoffer.com/making-a-robust-way-to-sync-data-from-airtables-to-mongodb-using-python-etl-solution/',
'https://insights.blackcoffer.com/incident-duration-prediction-infrastructure-and-real-estate/',
'https://insights.blackcoffer.com/statistical-data-analysis-of-reinforced-concrete/',
'https://insights.blackcoffer.com/database-normalization-segmentation-with-google-data-studio-dashboard-insights/',
'https://insights.blackcoffer.com/power-bi-dashboard-to-drive-insights-from-complex-data-to-generate-business-insights/',
'https://insights.blackcoffer.com/real-time-dashboard-to-monitor-infrastructure-activity-and-machines/',
'https://insights.blackcoffer.com/electric-vehicles-ev-load-management-system-to-forecast-energy-demand/',
'https://insights.blackcoffer.com/power-bi-data-driven-map-dashboard/',
'https://insights.blackcoffer.com/google-local-service-ads-lsa-leads-dashboard/',
'https://insights.blackcoffer.com/aws-lex-voice-and-chatbot/',
'https://insights.blackcoffer.com/metabridges-api-decentraland-integration/',
'https://insights.blackcoffer.com/microsoft-azure-chatbot-with-luis-language-understanding/',
'https://insights.blackcoffer.com/impact-of-news-media-and-press-on-innovation-startups-and-investments/',
'https://insights.blackcoffer.com/aws-quicksight-reporting-dashboard/',
'https://insights.blackcoffer.com/google-data-studio-dashboard-for-marketing-ads-and-traction-data/',
'https://insights.blackcoffer.com/gangala-in-e-commerce-big-data-etl-elt-solution-and-data-warehouse/',
'https://insights.blackcoffer.com/big-data-solution-to-an-online-multivendor-marketplace-ecommerce-business/',
'https://insights.blackcoffer.com/creating-a-custom-report-and-dashboard-using-the-data-got-from-atera-api/',
'https://insights.blackcoffer.com/azure-data-lake-and-power-bi-dashboard/',
'https://insights.blackcoffer.com/google-data-studio-pipeline-with-gcp-mysql/',
'https://insights.blackcoffer.com/quickbooks-dashboard-to-find-patterns-in-finance-sales-and-forecasts/',
'https://insights.blackcoffer.com/marketing-sales-and-financial-data-business-dashboard-wink-report/',
'https://insights.blackcoffer.com/react-native-apps-in-the-development-portfolio/',
'https://insights.blackcoffer.com/a-leading-firm-website-seo-optimization/',
'https://insights.blackcoffer.com/a-leading-hospitality-firm-in-the-usa-website-seo-optimization/',
'https://insights.blackcoffer.com/a-leading-firm-in-the-usa-website-seo-optimization/',
'https://insights.blackcoffer.com/a-leading-musical-instrumental-website-seo-optimization/',
'https://insights.blackcoffer.com/a-leading-firm-in-the-usa-seo-and-website-optimization/',
'https://insights.blackcoffer.com/immigration-datawarehouse-ai-based-recommendations/',
'https://insights.blackcoffer.com/lipsync-automation-for-celebrities-and-influencers/',
'https://insights.blackcoffer.com/key-audit-matters-predictive-modeling/',
'https://insights.blackcoffer.com/splitting-of-songs-into-its-vocals-and-instrumental/',
'https://insights.blackcoffer.com/ai-and-ml-technologies-to-evaluate-learning-assessments/',
'https://insights.blackcoffer.com/datawarehouse-and-recommendations-engine-for-airbnb/',
'https://insights.blackcoffer.com/real-estate-data-warehouse/',
'https://insights.blackcoffer.com/traction-dashboards-of-marketing-campaigns-and-posts/',
'https://insights.blackcoffer.com/google-local-service-ads-lsa-data-warehouse/',
'https://insights.blackcoffer.com/google-local-service-ads-missed-calls-and-messages-automation-tool/',
'https://insights.blackcoffer.com/marketing-ads-leads-call-status-data-tool-to-bigquery/',
'https://insights.blackcoffer.com/marketing-analytics-to-automate-leads-call-status-and-reporting/',
'https://insights.blackcoffer.com/callrail-analytics-leads-report-alert/',
'https://insights.blackcoffer.com/marketing-automation-tool-to-notify-lead-details-to-clients-over-email-and-phone/',
'https://insights.blackcoffer.com/data-etl-local-service-ads-leads-to-bigquery/',
'https://insights.blackcoffer.com/marbles-stimulation-using-python/',
'https://insights.blackcoffer.com/stocktwits-data-structurization/',
'https://insights.blackcoffer.com/sentimental-analysis-on-shareholder-letter-of-companies/',
'https://insights.blackcoffer.com/population-and-community-survey-of-america/',
'https://insights.blackcoffer.com/google-lsa-api-data-automation-and-dashboarding/',
'https://insights.blackcoffer.com/healthcare-data-analysis/',
'https://insights.blackcoffer.com/budget-sales-kpi-dashboard-using-power-bi/',
'https://insights.blackcoffer.com/amazon-buy-bot-an-automation-ai-tool-to-auto-checkouts/',
]

output_dir = 'selenium_articles'
os.makedirs(output_dir, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

driver_path = r'C:\Users\KIIT\OneDrive\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

def extract_article_text(html):
   
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup(['header', 'footer', 'nav', 'aside']):
        tag.decompose()

    selectors = ['article', 'main', '#content', '#main-content', '#article-body', '#post-content', '#story-body']
    for selector in selectors:
        content = soup.select_one(selector)
        if content and content.get_text(strip=True):
            return content.get_text(separator='\n', strip=True)

    return soup.get_text(separator='\n', strip=True)

articles = []
for i, url in enumerate(urls, 1):
    try:
        print(f"[{i}/{len(urls)}] Fetching: {url}")
        driver.get(url)
        time.sleep(2) 
        html = driver.page_source
        text = extract_article_text(html)
        articles.append({'url': url, 'content': text})
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        articles.append({'url': url, 'content': ''})


driver.quit()

for i, article in enumerate(articles, 1):
    df = pd.DataFrame([article])
    output_file = os.path.join(output_dir, f'article{i}.csv')
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Saved article {i} to {output_file}")
# seo_auditor/auditor.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import Counter
import subprocess
import json
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class SEOAuditor:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.metrics = {}

    def setup_driver():
        options = Options()
        options.headless = True  # Run in headless mode
        driver = webdriver.Chrome(options=options)
        return driver
    
    def fetch_page(self, use_selenium=False):
        if use_selenium:
            self.fetch_page_with_selenium()
        else:
            response = requests.get(self.url,verify=False)
            self.soup = BeautifulSoup(response.text, 'html.parser')

    def fetch_page_with_selenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        
        driver = webdriver.Chrome()
        driver.get(self.url)
        page_source = driver.page_source
        driver.quit()
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def check_meta_tags(self):
        title = self.soup.find('title')
        self.metrics['title'] = title.text if title else 'Missing'
        self.metrics['title_length'] = len(self.metrics['title'])

        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        self.metrics['meta_description'] = meta_desc['content'] if meta_desc else 'Missing'
        self.metrics['meta_description_length'] = len(self.metrics['meta_description']) if meta_desc else 0

    def check_headings(self):
        for i in range(1, 7):
            self.metrics[f'h{i}_count'] = len(self.soup.find_all(f'h{i}'))

    def check_images(self):
        images = self.soup.find_all('img')
        self.metrics['total_images'] = len(images)
        self.metrics['images_without_alt'] = sum(1 for img in images if not img.get('alt'))

    def analyze_keywords(self, target_keyword):
        text = self.soup.get_text().lower()
        words = re.findall(r'\w+', text)
        word_freq = Counter(words)
        total_words = len(words)

        self.metrics['keyword_frequency'] = word_freq[target_keyword.lower()]
        self.metrics['keyword_density'] = (self.metrics['keyword_frequency'] / total_words) * 100 if total_words > 0 else 0

    def run_lighthouse_audit(self):
        command = f"lighthouse {self.url} --output=json --quiet --chrome-flags='--headless'"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        try:
            lighthouse_results = json.loads(stdout)
            self.metrics['performance_score'] = lighthouse_results['categories']['performance']['score'] * 100
            self.metrics['accessibility_score'] = lighthouse_results['categories']['accessibility']['score'] * 100
            self.metrics['best_practices_score'] = lighthouse_results['categories']['best-practices']['score'] * 100
            self.metrics['seo_score'] = lighthouse_results['categories']['seo']['score'] * 100

            # Core Web Vitals
            self.metrics['largest_contentful_paint'] = lighthouse_results['audits']['largest-contentful-paint']['displayValue']
            self.metrics['first_input_delay'] = lighthouse_results['audits']['max-potential-fid']['displayValue']
            self.metrics['cumulative_layout_shift'] = lighthouse_results['audits']['cumulative-layout-shift']['displayValue']

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing Lighthouse results: {e}")

    def test_mobile_friendly(self):
        mobile_emulation = { "deviceName": "iPhone X" }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        page_source = driver.page_source
        driver.quit()
        self.metrics['mobile_friendly'] = 'Yes' if 'viewport' in page_source else 'No'

    def check_broken_links(self):
        driver = webdriver.Chrome()  # Assuming you already initialized the Chrome WebDriver
        driver.get(self.url)
    
        # Updated method to find links using By.TAG_NAME
        links = driver.find_elements(By.TAG_NAME, 'a')
    
        broken_links = []
        for link in links:
            url = link.get_attribute('href')
            if url:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code != 200:
                        broken_links.append(url)
                except requests.RequestException:
                    broken_links.append(url)
    
        driver.quit()
        self.metrics['broken_links'] = broken_links
        
    #Checks social tags    
    def check_social_tags(self):
        og_title = self.soup.find('meta', attrs={'property': 'og:title'})
        twitter_title = self.soup.find('meta', attrs={'name': 'twitter:title'})
    
        self.metrics['og_title'] = og_title['content'] if og_title else 'Missing'
        self.metrics['twitter_title'] = twitter_title['content'] if twitter_title else 'Missing'
    
    #Checks if wesbite is secured
    def check_https(self):
        parsed_url = urlparse(self.url)
        self.metrics['is_https'] = 'Yes' if parsed_url.scheme == 'https' else 'No'
    
    #Checks internal and external links
    def check_internal_external_links(self):
        links = [a['href'] for a in self.soup.find_all('a', href=True)]
        parsed_base = urlparse(self.url)
    
        internal_links = [link for link in links if urlparse(link).netloc == parsed_base.netloc]
        external_links = [link for link in links if urlparse(link).netloc != parsed_base.netloc]
    
        self.metrics['internal_links'] = len(internal_links)
        self.metrics['external_links'] = len(external_links)

    def generate_heading_graph(self):
        heading_counts = [self.metrics[f'h{i}_count'] for i in range(1, 7)]
        headings = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']

        plt.figure(figsize=(8, 5))
        plt.bar(headings, heading_counts, color='skyblue')
        plt.xlabel('Headings')
        plt.ylabel('Count')
        plt.title('Headings Count (H1 - H6)')
        plt.savefig('reports/heading_graph.png')
        plt.close()

    def generate_keyword_density_graph(self):
        labels = ['Target Keyword Density', 'Other Content']
        sizes = [self.metrics['keyword_density'], 100 - self.metrics['keyword_density']]

        plt.figure(figsize=(8, 5))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        plt.title('Keyword Density')
        plt.savefig('reports/keyword_density_graph.png')
        plt.close()

    def run_audit(self, target_keyword, use_selenium=False):
        self.fetch_page(use_selenium=use_selenium)
        self.check_meta_tags()
        self.check_headings()
        self.check_images()
        self.analyze_keywords(target_keyword)
        self.run_lighthouse_audit()

        # Additional Selenium-Based Features
        self.test_mobile_friendly()
        self.check_broken_links()
        self.check_social_tags()
        self.check_https()
        self.check_internal_external_links()
        
        #Graphs
        self.generate_heading_graph()  
        self.generate_keyword_density_graph() 

        return self.metrics
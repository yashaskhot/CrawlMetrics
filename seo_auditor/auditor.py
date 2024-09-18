# seo_auditor/auditor.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from collections import Counter
import subprocess
import json

class SEOAuditor:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.metrics = {}

    def fetch_page(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

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

    def run_audit(self, target_keyword):
        self.fetch_page()
        self.check_meta_tags()
        self.check_headings()
        self.check_images()
        self.analyze_keywords(target_keyword)
        self.run_lighthouse_audit()
        return self.metrics
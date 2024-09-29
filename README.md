
# Crawl Metrics

Crawl Metrics is an SEO auditing tool built in Python. It crawls websites, checks various SEO metrics (such as meta tags, keyword density, headings, and images), and runs performance audits using Google's Lighthouse tool. This tool helps you analyze and optimize your website's SEO performance.

## Features
- Check for meta tags like title and meta description
- Analyze the frequency and density of target keywords
- Count headings (h1-h6) and images, and identify images without alt text
- Perform Lighthouse audits for performance, accessibility, best practices, and SEO
- Display Core Web Vitals (LCP, FID, CLS)
- Heading Distribution Graph (H1 to H6).
- HTTPS Check for secure connections.
- Internal and External Links Count.
= Broken Links Detection.
- Mobile-Friendliness Test.
- Meta Tags Analysis (title, description).
- Keyword Frequency and Density Analysis.

## Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yashaskhot/crawlmetrics.git
cd crawlmetrics
```

### 2. Set up a Python Virtual Environment

Create a virtual environment to manage dependencies.
```bash
# For Linux/macOS
python3 -m venv env
source env/bin/activate

# For Windows
python -m venv env
.\env\Scripts\activate
```

### 3. Install Python Dependencies

Use `pip` to install the required dependencies from `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Install Lighthouse Globally

Crawl Metrics relies on Google's Lighthouse for performance and SEO audits. You need to install Lighthouse globally using `npm`.

```bash
npm install -g lighthouse
```

Ensure you have [Node.js](https://nodejs.org/) installed before running this command.

### 5. Running the Tool

To run the SEO auditor, use the following command syntax:

```bash
python run_audit.py <URL> <TARGET_KEYWORD>
```

- `<URL>`: The URL of the website you want to audit (e.g., `https://example.com`).
- `<TARGET_KEYWORD>`: The keyword to check for frequency and density on the page.

Example:

```bash
python run_audit.py https://example.com example-keyword
```

## Example Output
The tool will return various metrics, including:
- Meta tags (title, description, and their lengths)
- Heading count (h1, h2, h3, etc.)
- Images count and those without `alt` attributes
- Keyword frequency and density
- Lighthouse performance metrics like SEO score, accessibility score, and Core Web Vitals (LCP, FID, CLS)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you'd like to contribute to Crawl Metrics, feel free to open an issue or submit a pull request.

## OpenSource Libraries Used
- beautifulsoup4
- reportlab
- Requests
- lighthouse
---

Happy crawling and optimizing!

# run_audit.py

import argparse
from seo_auditor.auditor import SEOAuditor
from seo_auditor.report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description="Run an SEO audit on a specified URL")
    parser.add_argument("url", help="The URL to audit")
    parser.add_argument("keyword", help="The target keyword to analyze")
    args = parser.parse_args()

    auditor = SEOAuditor(args.url)
    metrics = auditor.run_audit(args.keyword)
    report_path = generate_report(args.url, args.keyword, metrics)

    print(f"Audit complete. Report saved to: {report_path}")

if __name__ == "__main__":
    main()
# seo_auditor/report_generator.py

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
from datetime import datetime

def generate_report(url, keyword, metrics):
    report_dir = 'reports'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    filename = f"{report_dir}/seo_audit_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"SEO Audit Report for {url}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Keyword
    elements.append(Paragraph(f"Target Keyword: {keyword}", styles['Heading2']))
    elements.append(Spacer(1, 12))

    # Metrics Table Data
    data = [["Metric", "Value"]]

    # Add HTTPS check result
    data.append(["Is HTTPS?", metrics.get('is_https', 'Not checked')])

    # Add internal and external links
    data.append(["Internal Links", metrics.get('internal_links', 'Not checked')])
    data.append(["External Links", metrics.get('external_links', 'Not checked')])

    # Handle long "Broken Links" with Paragraph for proper wrapping
    broken_links = metrics.get('broken_links', 'Not checked')
    if isinstance(broken_links, list):
        # If broken_links is a list, format it into a Paragraph
        broken_links_paragraph = Paragraph("<br />".join(broken_links), styles['Normal'])
    else:
        # In case broken_links is not a list, handle it as a string
        broken_links_paragraph = Paragraph(str(broken_links), styles['Normal'])
    data.append(["Broken Links", broken_links_paragraph])

    # Wrap long values in Paragraph for proper text wrapping
    for key, value in metrics.items():
        if key not in ['is_https', 'internal_links', 'external_links', 'broken_links']:  # Already included above
            # Wrap the long text (e.g., Meta Description) in a Paragraph to handle overflow
            formatted_value = Paragraph(str(value), styles['Normal']) if isinstance(value, str) else str(value)
            data.append([key.replace('_', ' ').title(), formatted_value])

    # Create the table with dynamic column widths (metric column has fixed width, value column is flexible)
    table = Table(data, colWidths=[2.5 * inch, 4 * inch])  # Adjust column width here
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 1), (-1, -1), 'TOP')  # Align text to the top for better readability
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Embed Heading Count Graph
    heading_graph_path = "reports/heading_graph.png"
    if os.path.exists(heading_graph_path):
        elements.append(Paragraph("Headings Count Graph (H1-H6):", styles['Heading2']))
        elements.append(Spacer(1, 12))
        elements.append(Image(heading_graph_path, width=300, height=150))
        elements.append(Spacer(1, 24))

    # Embed Keyword Density Graph
    keyword_density_graph_path = "reports/keyword_density_graph.png"
    if os.path.exists(keyword_density_graph_path):
        elements.append(Paragraph("Keyword Density Graph:", styles['Heading2']))
        elements.append(Spacer(1, 12))
        elements.append(Image(keyword_density_graph_path, width=300, height=150))
        elements.append(Spacer(1, 24))

    # Build the report PDF
    doc.build(elements)
    return filename


# seo_auditor/report_generator.py

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# import os
# from datetime import datetime

# def generate_report(url, keyword, metrics):
#     report_dir = 'reports'
#     if not os.path.exists(report_dir):
#         os.makedirs(report_dir)

#     filename = f"{report_dir}/seo_audit_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     doc = SimpleDocTemplate(filename, pagesize=letter)
#     styles = getSampleStyleSheet()
#     elements = []

#     # Title
#     elements.append(Paragraph(f"SEO Audit Report for {url}", styles['Title']))
#     elements.append(Spacer(1, 12))

#     # Keyword
#     elements.append(Paragraph(f"Target Keyword: {keyword}", styles['Heading2']))
#     elements.append(Spacer(1, 12))

#     # Metrics Table
#     data = [["Metric", "Value"]]

#     # Add HTTPS check result
#     data.append(["Is HTTPS?", metrics.get('is_https', 'Not checked')])

#     # Add internal and external links
#     data.append(["Internal Links", metrics.get('internal_links', 'Not checked')])
#     data.append(["External Links", metrics.get('external_links', 'Not checked')])

#     # Add any other metrics from the SEO audit (existing)
#     for key, value in metrics.items():
#         if key not in ['is_https','internal_links', 'external_links']:  # Already included above
#             data.append([key.replace('_', ' ').title(), str(value)])

#     # Create the table
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 14),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
#         ('FONTSIZE', (0, 0), (-1, -1), 12),
#         ('TOPPADDING', (0, 0), (-1, -1), 6),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))
#     elements.append(table)

#     # Build the report PDF
#     doc.build(elements)
#     return filename

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
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

    # Metrics Table
    data = [["Metric", "Value"]]

    # Add HTTPS check result
    data.append(["Is HTTPS?", metrics.get('is_https', 'Not checked')])

    # Add internal and external links
    data.append(["Internal Links", metrics.get('internal_links', 'Not checked')])
    data.append(["External Links", metrics.get('external_links', 'Not checked')])

    # Add any other metrics from the SEO audit (existing)
    for key, value in metrics.items():
        if key not in ['is_https','internal_links', 'external_links']:  # Already included above
            data.append([key.replace('_', ' ').title(), str(value)])

    # Create the table
    table = Table(data)
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
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Embed Heading Count Graph
    heading_graph_path = "reports/heading_graph.png"
    if os.path.exists(heading_graph_path):
        elements.append(Paragraph("Headings Count Graph (H1-H6):", styles['Heading2']))
        elements.append(Spacer(1, 12))
        elements.append(Image(heading_graph_path, width=400, height=200))
        elements.append(Spacer(1, 24))

    # Embed Keyword Density Graph
    keyword_density_graph_path = "reports/keyword_density_graph.png"
    if os.path.exists(keyword_density_graph_path):
        elements.append(Paragraph("Keyword Density Graph:", styles['Heading2']))
        elements.append(Spacer(1, 12))
        elements.append(Image(keyword_density_graph_path, width=400, height=200))
        elements.append(Spacer(1, 24))

    # Build the report PDF
    doc.build(elements)
    return filename

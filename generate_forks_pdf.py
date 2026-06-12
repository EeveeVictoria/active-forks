#!/usr/bin/env python3
"""
Generate a PDF report of all your GitHub forks with detailed information.
Requires: pip install PyGithub reportlab
"""

import os
from datetime import datetime
from github import Github
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def get_forks(username, token=None):
    """Fetch all forked repositories for a user."""
    if token:
        g = Github(token)
    else:
        g = Github()
    
    user = g.get_user(username)
    forks = []
    
    print(f"Fetching forks for {username}...")
    for repo in user.get_repos(type="owner"):
        if repo.fork:
            # Get original repo info
            original_repo = repo.source
            
            forks.append({
                'name': repo.name,
                'url': repo.html_url,
                'description': repo.description or 'No description',
                'stars': original_repo.stargazers_count,  # Stars from original repo
                'language': repo.language or 'N/A',
                'created_at': original_repo.created_at.strftime('%Y-%m-%d') if original_repo.created_at else 'N/A',  # Created from original repo
                'fork_created_at': repo.created_at.strftime('%Y-%m-%d') if repo.created_at else 'N/A',
                'forks_count': original_repo.forks_count,  # Forks from original repo
                'open_issues': original_repo.open_issues_count,  # Issues from original repo
                'original_url': original_repo.html_url,
            })
    
    return sorted(forks, key=lambda x: x['created_at'], reverse=True)


def create_pdf(forks, username, output_filename='forks_report.pdf'):
    """Create a PDF report of forks."""
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0366d6'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#586069'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph(f"GitHub Forks Report for {username}", title_style)
    elements.append(title)
    
    # Subtitle with generation date
    subtitle = Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>Total Forks: {len(forks)}",
        subtitle_style
    )
    elements.append(subtitle)
    elements.append(Spacer(1, 0.2*inch))
    
    # Prepare table data with wrapped text
    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        alignment=TA_LEFT
    )
    
    table_data = [['Repository', 'Description', 'Stars\n(Original)', 'Language', 'Created\n(Original)']]
    
    for fork in forks:
        # Truncate description if too long
        desc = fork['description']
        if len(desc) > 50:
            desc = desc[:47] + '...'
        
        # Create paragraph for description to handle wrapping
        desc_para = Paragraph(desc, cell_style)
        
        table_data.append([
            fork['name'],
            desc_para,
            str(fork['stars']),
            fork['language'],
            fork['created_at']
        ])
    
    # Create table with adjusted column widths
    table = Table(table_data, colWidths=[1.0*inch, 2.2*inch, 0.75*inch, 0.75*inch, 1.0*inch])
    
    # Style table
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0366d6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 1), (-1, -1), 6),
        ('RIGHTPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f6f8fa')]),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5da')),
        ('LEFTPADDING', (1, 0), (1, -1), 8),
        ('RIGHTPADDING', (1, 0), (1, -1), 8),
    ]))
    
    elements.append(table)
    
    # Add detailed list on new pages
    elements.append(PageBreak())
    elements.append(Paragraph("Detailed Repository Information", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    detail_style = ParagraphStyle(
        'DetailStyle',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=4,
        textColor=colors.HexColor('#24292e'),
        leading=12
    )
    
    for i, fork in enumerate(forks, 1):
        # Repo name and link
        name_style = ParagraphStyle(
            'RepoName',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#0366d6'),
            spaceAfter=4
        )
        
        elements.append(Paragraph(f"{i}. {fork['name']}", name_style))
        
        # Details
        details = f"""
        <b>Your Fork URL:</b> {fork['url']}<br/>
        <b>Original Repo URL:</b> {fork['original_url']}<br/>
        <b>Description:</b> {fork['description']}<br/>
        <b>Stars (Original):</b> {fork['stars']} | <b>Forks (Original):</b> {fork['forks_count']} | <b>Open Issues (Original):</b> {fork['open_issues']}<br/>
        <b>Language:</b> {fork['language']} | <b>Original Created:</b> {fork['created_at']} | <b>Your Fork Created:</b> {fork['fork_created_at']}<br/>
        """
        
        elements.append(Paragraph(details, detail_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Add page break every 5 repos for readability
        if (i % 5 == 0) and (i < len(forks)):
            elements.append(PageBreak())
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF generated: {output_filename}")


def main():
    """Main function."""
    import sys
    
    # Configuration
    USERNAME = 'EeveeVictoria'  # Change this to your username
    TOKEN = os.getenv('GITHUB_TOKEN')  # Optional: use personal access token for higher rate limits
    OUTPUT_FILE = 'forks_report.pdf'
    
    try:
        # Fetch forks
        forks = get_forks(USERNAME, TOKEN)
        
        if not forks:
            print("No forks found!")
            return
        
        print(f"Found {len(forks)} forks")
        
        # Create PDF
        create_pdf(forks, USERNAME, OUTPUT_FILE)
        print(f"\n📄 Report saved to: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

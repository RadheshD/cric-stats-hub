import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from file_manager import read_json

def generate_pdf_report(json_file, charts_dir, pdf_file):
    """Generate a PDF report for the match."""
    data = read_json(json_file)
    if not data:
        return

    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']

    # Custom style for bold text
    bold_style = ParagraphStyle('Bold', parent=styles['Normal'], fontName='Helvetica-Bold')

    story = []

    # Title
    match_details = data['match_details']
    story.append(Paragraph(f"Match Report: {match_details['match']}", title_style))
    story.append(Paragraph(f"Tournament: {match_details['tournament']}", subtitle_style))
    story.append(Spacer(1, 12))

    # Match Details
    story.append(Paragraph(f"<b>Date:</b> {match_details['date']}", normal_style))
    story.append(Paragraph(f"<b>Venue:</b> {match_details['venue']}", normal_style))
    story.append(Paragraph(f"<b>Toss:</b> {match_details['toss']}", normal_style))
    story.append(Paragraph(f"<b>Result:</b> {match_details['result']}", normal_style))
    story.append(Spacer(1, 12))

    # Team Scores
    story.append(Paragraph("Team Scores", subtitle_style))
    score_data = [['Team', 'Runs', 'Wickets', 'Overs', 'Status']]
    for team, stats in data['team_scores'].items():
        score_data.append([team, stats['runs'], stats['wickets'], stats['overs'], stats['status']])
    
    score_table = Table(score_data, colWidths=[100, 80, 80, 80, 80])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 12))

    # Batting Stats - India
    story.append(Paragraph("India - Top Batting Stats", subtitle_style))
    ind_bat_data = [['Player', 'Runs', 'Status']]
    for player in data['batting_stats']['India']:
        ind_bat_data.append([player['player'], player['runs'], player['status']])
    
    ind_bat_table = Table(ind_bat_data, colWidths=[150, 80, 100])
    ind_bat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(ind_bat_table)
    story.append(Spacer(1, 12))

    # Bowling Stats - Australia
    story.append(Paragraph("Australia - Top Bowling Stats", subtitle_style))
    aus_bowl_data = [['Bowler', 'Wickets']]
    for bowler in data['bowling_stats']['Australia']:
        aus_bowl_data.append([bowler['bowler'], bowler['wickets']])
    
    aus_bowl_table = Table(aus_bowl_data, colWidths=[150, 80])
    aus_bowl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(aus_bowl_table)
    story.append(Spacer(1, 12))

    # Include Charts
    story.append(Paragraph("Match Visualizations", subtitle_style))
    
    chart_files = [
        ('team_score_chart.png', 400, 250),
        ('india_batting_contribution_pie_chart.png', 300, 300),
        ('australia_batting_contribution_pie_chart.png', 300, 300),
        ('australia_bowling_wickets_chart.png', 400, 250),
        ('india_bowling_wickets_chart.png', 400, 250)
    ]
    
    for chart_file, w, h in chart_files:
        chart_path = os.path.join(charts_dir, chart_file)
        if os.path.exists(chart_path):
            img = Image(chart_path, width=w, height=h)
            story.append(img)
            story.append(Spacer(1, 12))

    # Build PDF
    doc.build(story)
    print(f"Generated PDF report at {pdf_file}")

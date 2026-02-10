def daily_summary_email_template(summary_data: dict) -> str:
    """
    Returns HTML formatted daily summary email
    """
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>Daily Lead Summary</h2>
        <p>Here is your lead summary for yesterday:</p>
        <ul>
          <li><strong>Retarget:</strong> {summary_data['retarget']}</li>
          <li><strong>Contacted:</strong> {summary_data['contacted']}</li>
          <li><strong>Meetings:</strong> {summary_data['meetings']}</li>
          <li><strong>Scraped:</strong> {summary_data['scraped']}</li>
        </ul>
        <p>Keep up the great work!</p>
      </body>
    </html>
    """
    return html

import smtplib
import configuration

from email.mime.text import MIMEText

def send_release_mail(recipients, date, subject):
    smtp_server = 'smtp.gmail.com'
    port = 587
    from_email = 'Movie Release Tracker <MovieReleaseTracker@Gmail>'
    message = f"<h3>{subject} Comes Out Today, {date}!</h3>"

    msg = MIMEText(message, 'html')
    msg['From'] = from_email
    msg['To'] = recipients
    msg['Subject'] = subject

    # msg_str = msg.as_string()
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()

    server.login(configuration.EMAIL_USERNAME, configuration.EMAIL_PASSWORD)
    server.sendmail(from_email, recipients, msg.as_string())
    server.quit()
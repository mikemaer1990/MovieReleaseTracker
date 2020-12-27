import smtplib
import configuration

from email.mime.text import MIMEText

# function that sends an eamil from our SMTP server
def send_release_mail(recipients, date, subject):
    # set values for the smtplib sendmail function
    smtp_server = 'smtp.gmail.com'
    port = 587
    from_email = 'Movie Release Tracker <MovieReleaseTracker@Gmail>'
    message = f"<h3>{subject} Comes Out Today, {date}!</h3>"

    # msg sections
    msg = MIMEText(message, 'html')
    msg['From'] = from_email
    msg['To'] = recipients
    msg['Subject'] = subject

    # set up connection
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    
    # login and send mail
    server.login(configuration.EMAIL_USERNAME, configuration.EMAIL_PASSWORD)
    server.sendmail(from_email, recipients, msg.as_string())
    server.quit()
import smtplib
import configuration

from email.mime.text import MIMEText
from flask import url_for

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

# function that sends an eamil from our SMTP server to reset password
def send_reset_mail(recipients, reset_token, link):
    # set values for the smtplib sendmail function
    smtp_server = 'smtp.gmail.com'
    port = 587
    from_email = 'Movie Release Tracker <MovieReleaseTracker@Gmail>'
    email_link = link
    message = f'<h2><a href="{email_link}">Click here to reset your password</h2></a>\
                <p>If you didn\'t request this email, please ignore and nothing will be changed.<p>'

    # msg sections - add html as a second argument to chg to html
    msg = MIMEText(message, 'html')
    msg['From'] = from_email
    msg['To'] = recipients
    msg['Subject'] = 'Password Reset Request'

    # set up connection
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    
    # login and send mail
    server.login(configuration.EMAIL_USERNAME, configuration.EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

def send_confirmation_email(to, confirm_url):
    # set values for the smtplib sendmail function
    smtp_server = 'smtp.gmail.com'
    port = 587
    from_email = 'Movie Release Tracker <MovieReleaseTracker@Gmail>'
    confirm_url = confirm_url
    message = f'<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>\
                <p><a href="{ confirm_url }">{ confirm_url }</a></p>\
                <br>\
                <p>Cheers! 🍻</p>'

    # msg sections - add html as a second argument to chg to html
    msg = MIMEText(message, 'html')
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = 'MovieReleaseTracker Email Confirmation'

    # set up connection
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    
    # login and send mail
    server.login(configuration.EMAIL_USERNAME, configuration.EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()


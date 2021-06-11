import smtplib, ssl
import configuration

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# function that sends an eamil from our SMTP server
def send_release_mail(recipients, date, subject, img_url, cast):
    # set values for the smtplib sendmail function
    from_email = 'Movie Release Tracker <MovieReleaseTracker@Gmail>'

    # Set cast values for email template
    castOne = cast[0]['name'] or 'N/A'
    castTwo = cast[1]['name'] or 'N/A'

    # Create our multipart elemet
    msg = MIMEMultipart("alternative")
    msg['From'] = from_email
    msg['To'] = recipients
    msg['Subject'] = f"MRT Release Notification - {subject}"

    # Create the plain text version of the email
    text = f"{subject} Comes Out Today, {date}!\
            Starring: {castOne} and {castTwo}\
            <a href='https://moviereleasetracker.herokuapp.com/user/follows'>Click here to view your follows</a>\
        "
        
    # Create the html version of the email
    html = f"<div style='color: white;margin:auto;border:4px ridge gray; max-width: 400px; text-align:center;background-color:#1c1f23;font-size:calc(10px + 0.25vw); font-weight: bold;'>\
                <div style='display: flex; justify-content: center; align-items: center; height: 3rem;'>\
                    <h3 style='margin: auto;'>{subject} Comes Out Today, {date}!</h3>\
                </div>\
                <div style='padding:1.5rem 0 0.5rem 0;background-color:#1C6E8C'>\
                    <a href='https://www.watchplaystream.com/en/search/{subject}.html'><img style='border-radius: 0.5rem;' src='{img_url}' width=100 height=150></a>\
                    <p>Starring: {castOne} and {castTwo}</p>\
                </div>\
                <div style='padding: 0 0 0.5rem 0;'>\
                    <p>Click the image above to see where you can watch it.</p>\
                    <a href='https://moviereleasetracker.herokuapp.com/user/follows'>Click here to view your follows</a>\
                </div>\
            </div>"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(configuration.EMAIL_USERNAME, configuration.EMAIL_PASSWORD)
        server.sendmail(
            from_email, recipients, msg.as_string()
        )

# function that sends an eamil from our SMTP server to reset password
def send_reset_mail(recipients, reset_token, link):
    # set values for the smtplib sendmail function
    from_email = 'Movie Release Tracker <MovieReleaseTracker@Gmail>'
    email_link = link
    message = f'<h2><a href="{email_link}">Click here to reset your password</h2></a>\
                <p>If you didn\'t request this email, please ignore and nothing will be changed.<p>'

    # msg sections - add html as a second argument to chg to html
    msg = MIMEText(message, 'html')
    msg['From'] = from_email
    msg['To'] = recipients
    msg['Subject'] = 'Password Reset Request'

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(configuration.EMAIL_USERNAME, configuration.EMAIL_PASSWORD)
        server.sendmail(
            from_email, recipients, msg.as_string()
        )

# Function to send users email confirmations to authorize their account
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
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(configuration.EMAIL_USERNAME, configuration.EMAIL_PASSWORD)
        server.sendmail(
            from_email, to, msg.as_string()
        )
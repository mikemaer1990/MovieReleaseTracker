import configuration
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# function that sends an eamil from our SMTP server
def send_release_mail(recipients, date, subject, img_url, cast):

    # Set cast values for email template
    castOne = cast[0]['name'] or 'N/A'
    castTwo = cast[1]['name'] or 'N/A'

    message = Mail(
        from_email = "MovieReleaseTracker@Gmail.com",
        to_emails = recipients,
        subject = f"MRT Release Notification - {subject}",
        # plain_content = f"{subject} Comes Out Today, {date}!\
        #     Starring: {castOne} and {castTwo}\
        #     <a href='https://moviereleasetracker.herokuapp.com/user/follows'>Click here to view your follows</a>\
        # ",
        html_content = f"<div style='color: white;margin:auto;border:4px ridge gray; max-width: 400px; text-align:center;background-color:#1c1f23;font-size:calc(10px + 0.25vw); font-weight: bold;'>\
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
        )
    try:
        sg = SendGridAPIClient(configuration.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


# function that sends an eamil from our SMTP server to reset password via SendGrid // https://app.sendgrid.com/
def send_reset_mail(recipients, link):
    message = Mail(
        from_email='MovieReleaseTracker@Gmail.com',
        to_emails=recipients,
        subject='Password Reset',
        html_content=   f'<h2><a href="{ link }">Click here to reset your password</h2></a>\
                <p>If you didn\'t request this email, please ignore and nothing will be changed.<p>'
        )
    try:
        sg = SendGridAPIClient(configuration.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

# Function to send email confirmation to the user via SendGrid // https://app.sendgrid.com/
def send_confirmation_email(to, confirm_url):
    message = Mail(
        from_email='MovieReleaseTracker@Gmail.com',
        to_emails=to,
        subject='Confirmation Email',
        html_content=   f'<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p>\
                        <p><a href="{ confirm_url }">{ confirm_url }</a></p>\
                        <br>\
                        <p>Cheers! 🍻</p>'
        )
    try:
        sg = SendGridAPIClient(configuration.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


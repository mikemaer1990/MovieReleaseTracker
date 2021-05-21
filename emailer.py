import configuration
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# function that sends an eamil from our SMTP server
def send_release_mail(recipients, date, subject, img_url):
    message = Mail(
        from_email = "MovieReleaseTracker@Gmail.com",
        to_emails = recipients,
        subject = f"MRT Release Notification - {subject}",
        html_content = f"<div>\
            <h3>{subject} Comes Out Today, {date}!</h3>\
            <img src='{img_url}' width=50 height=50>\
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


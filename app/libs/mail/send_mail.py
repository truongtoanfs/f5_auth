import smtplib
from email.message import EmailMessage
from config import apiConfig
from app.libs.exception.service import SendEmailException


async def send_mail(receiver_email: str, password: str):
    with open("app/libs/mail/textfile.txt", "r") as file:
        file_content = file.read()

    sender_email = apiConfig.SENDER_EMAIL
    sender_email_password = apiConfig.SENDER_EMAIL_PASSWORD
    receiver_name = receiver_email.split("@")[0]
    file_content = file_content.replace("{{password}}", password)

    msg = EmailMessage()
    msg.set_content(file_content)
    msg["Subject"] = f"Hello, {receiver_name}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as session:
            session.starttls()
            session.login(sender_email, sender_email_password)
            session.send_message(msg)
            print(f"Email sent successfully to {receiver_name}!")
    except Exception:
        raise SendEmailException

import random
import smtplib
from email.mime.text import MIMEText

def send_otp(receiver_email):

    otp = random.randint(100000,999999)

    sender_email = "dambalekomal5@gmail.com"
    sender_password = "fjwguqhoqkdkfvwd"

    msg = MIMEText(f"Your OTP is {otp}")

    msg['Subject'] = 'JALNETRA OTP'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP('smtp.gmail.com',587)

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    server.send_message(msg)

    server.quit()

    return str(otp)
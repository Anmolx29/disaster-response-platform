"""
Disaster Alert Service
Supports SMS (Twilio), Email (SMTP), and placeholder for Push Notifications.
"""

import os
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

class AlertService:
    def __init__(self):
        # Load Twilio credentials from environment variables (.env file)
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))

    def send_sms(self, message, to_number):
        """Send an SMS alert using Twilio"""
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            msg = client.messages.create(body=message, from_=self.twilio_number, to=to_number)
            print(f"SMS sent to {to_number}: SID={msg.sid}")
            return True
        except Exception as e:
            print("Failed to send SMS:", e)
            return False

    def send_email(self, subject, message, to_email):
        """Send an email alert using SMTP"""
        try:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = self.email_address
            msg["To"] = to_email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print("Failed to send email:", e)
            return False

    def send_push(self, message, device_token):
        """Placeholder for sending push notification (mobile)"""
        print(f"Push notification (SIM): {message} to device {device_token}")
        return True

if __name__ == "__main__":
    # Example usage / test
    alert = AlertService()
    # Test SMS - you must have Twilio credentials & verified number to use this!
    # alert.send_sms("TEST ALERT: This is a drill", "+911234567890")
    # Test Email
    # alert.send_email("Test Alert", "This is only a test.", "someone@example.com")
    # Test Push (placeholder)
    alert.send_push("Danger: Area evacuated!", "+918477934986")

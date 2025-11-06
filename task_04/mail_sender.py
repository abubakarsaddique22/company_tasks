import smtplib
import time
import random
import csv
from email.mime.text import MIMEText

# Gmail credentials
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"  # from Google Account > Security > App Passwords

# Email subject
SUBJECT = "Application for Internship Opportunity"

# Read recipients from CSV
with open("recipients.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    recipients = list(reader)

# Connect to Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    print("✅ Logged in successfully!")

    for r in recipients:
        name = r["name"]
        email = r["email"]
        field = r["field"]

        # Personalized message
        message = f"""
Dear {name},

I hope you're doing well.

My name is Abubakar Saddique, and I am interested in an internship related to {field}.
I have experience with Python, data analysis, and problem solving, and I’m eager to apply my skills to real-world projects.

Please find my CV attached if required. I’d be grateful for an opportunity to contribute to your team.

Best regards,
Abubakar Saddique
📧 saddiqueabubakar642@gmail.com
📞 [your contact number]
"""

        msg = MIMEText(message)
        msg["Subject"] = SUBJECT
        msg["From"] = SENDER_EMAIL
        msg["To"] = email

        try:
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print(f"✅ Sent to {name} ({email})")
        except Exception as e:
            print(f"❌ Failed to send to {email}: {e}")
            with open("failed_emails.txt", "a") as f:
                f.write(email + "\n")

        # Delay between 60–120 seconds (randomized for safety)
        delay = random.randint(60, 120)
        print(f"⏳ Waiting {delay} seconds before next email...\n")
        time.sleep(delay)

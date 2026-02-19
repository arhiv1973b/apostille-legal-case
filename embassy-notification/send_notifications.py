#!/usr/bin/env python3
"""
Diplomatic Notification Sender
Sends legal case notifications to embassies of Hague Convention member states
"""

import csv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# Email templates
SUBJECT = "Legal Case Against Moldova - Human Rights Violations - Request for Support"

BODY_TEMPLATE = """
Excellency,

We respectfully request your attention to a serious case of human rights violations and judicial misconduct by the Republic of Moldova, a member state of the Hague Convention of 1961.

CASE SUMMARY
============
A civil lawsuit has been filed against the State of the Republic of Moldova seeking €500,000 in compensation for damages caused by:

1. Systematic violation of fair trial rights (Art. 6 ECHR)
2. Failure to investigate torture allegations (Art. 3 ECHR)
3. Denial of effective remedy (Art. 13 ECHR)
4. Illegal apostille certification of court decisions

The case involves 90 apostilles issued during 2021-2023, with 14.4% having unreadable signatures ("unclear signature"), indicating systemic procedural violations.

DOCUMENTATION
=============
All case documents are available at:
https://github.com/arhiv1973b/apostille-legal-case

Translations are available in: EN, RU, FR, DE, ES, PT, IT, PL, RO, UK, CN, AR

LEGAL BASIS
===========
- European Convention on Human Rights
- Hague Convention of 1961 (Apostille)
- Civil Code of the Republic of Moldova
- Rome Statute of the International Criminal Court (Art. 17)

REQUEST
=======
We kindly request:
1. Review of this case documentation
2. Support for human rights monitoring
3. Diplomatic intervention if violations are confirmed
4. Communication to your government about this matter

We count on your support in ensuring justice and accountability.

Respectfully,
Plaintiff

---
This notification is sent to all 126 member states of the Hague Convention of 1961
"""

# Embassy database (CSV format)
EMBASSY_DB = "embassies.csv"


def load_embassies():
    """Load embassy contacts from CSV"""
    embassies = []
    try:
        with open(EMBASSY_DB, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                embassies.append(row)
    except FileNotFoundError:
        print(f"Warning: {EMBASSY_DB} not found")
    return embassies


def send_email(to_email, country):
    """Send notification email to embassy"""
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"⚠️ SMTP not configured. Would send to {country}: {to_email}")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = SUBJECT

        msg.attach(MIMEText(BODY_TEMPLATE, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✓ Sent to {country}: {to_email}")
        return True
    except Exception as e:
        print(f"✗ Failed to send to {country}: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("DIPLOMATIC NOTIFICATION SENDER")
    print("=" * 60)
    print(f"Started: {datetime.now()}")
    print()

    embassies = load_embassies()
    print(f"Loaded {len(embassies)} embassy contacts")

    if not SMTP_USER:
        print("\n⚠️ SMTP not configured!")
        print("Set environment variables:")
        print("  SMTP_USER=your-email@gmail.com")
        print("  SMTP_PASSWORD=your-app-password")
        print("\nTo send test emails, run with configured SMTP")

    # Show first 5 embassies as preview
    print("\nPreview (first 5 embassies):")
    for embassy in embassies[:5]:
        print(f"  - {embassy.get('Country', 'Unknown')}: {embassy.get('Email', 'N/A')}")

    print("\n" + "=" * 60)
    print("To send all notifications, configure SMTP and run again")
    print("=" * 60)


if __name__ == "__main__":
    main()

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

# ============================================
# CONFIGURATION - Edit these values
# ============================================
SMTP_SERVER = "smtp.office365.com"  # Outlook/Office 365
SMTP_PORT = 587
SMTP_USER = "arhiv1973b@outlook.com"  # Your Outlook email
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # App password or regular password

# Email templates
SUBJECT = "Legal Case Against Moldova - Human Rights Violations - Request for Support"

BODY_TEMPLATE = """Excellency,

We respectfully request your attention to a serious case of human rights violations and judicial misconduct by the Republic of Moldova, a member state of the Hague Convention of 1961.

CASE SUMMARY
============
A civil lawsuit has been filed against the State of the Republic of Moldova seeking EUR 500,000 in compensation for damages caused by:

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
                if row.get("Email") and row.get("Email").strip():
                    embassies.append(row)
    except FileNotFoundError:
        print(f"Warning: {EMBASSY_DB} not found")
    return embassies


def send_email(to_email, country, from_email):
    """Send notification email to embassy"""
    if not SMTP_PASSWORD:
        print(f"⚠️ SMTP password not set. Would send to {country}: {to_email}")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
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
    print(f"From: {SMTP_USER}")
    print()

    embassies = load_embassies()
    print(f"Loaded {len(embassies)} embassy contacts with emails")

    if not SMTP_PASSWORD:
        print("\n⚠️ SMTP_PASSWORD not set!")
        print("Set environment variable:")
        print("  export SMTP_PASSWORD='your-password'")
        print("\nRun script again after setting password")
        return

    # Show embassies that will be notified
    print("\nEmbassies that will receive notification:")
    for embassy in embassies:
        print(f"  - {embassy.get('Country', 'Unknown')}: {embassy.get('Email', 'N/A')}")

    print("\n" + "=" * 60)

    # Send confirmation
    confirm = input(f"Send to {len(embassies)} embassies? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancelled.")
        return

    success = 0
    failed = 0

    for embassy in embassies:
        email = embassy.get("Email", "").strip()
        country = embassy.get("Country", "Unknown")

        if email and send_email(email, country, SMTP_USER):
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"COMPLETED: {success} sent, {failed} failed")
    print("=" * 60)


if __name__ == "__main__":
    main()

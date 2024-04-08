import requests
from bs4 import BeautifulSoup
import re
from email_validator import validate_email, EmailNotValidError


def find_emails(content):
    """Find emails in webpage content."""
    return list(
        set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content))
    )


def _validate_email(email):
    try:
        emailinfo = validate_email(email, check_deliverability=True)
        email = emailinfo.normalized
        return email

    except EmailNotValidError as e:
        print(str(e))
        return


def find_emails_on_contact_page(html_content, base_url):
    """Find emails on a contact page linked from the initial page."""
    valid_emails = []
    soup = BeautifulSoup(html_content, "html.parser")
    contact_links = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if "contact" in a["href"].lower()
    ]
    for link in contact_links:
        link = link if link.startswith("http") else base_url + link
        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                emails = find_emails(response.text)
                for email in emails:
                    validated_email = _validate_email(email)  # Validate each email
                    if validated_email:  # If email is valid, add to the list
                        valid_emails.append(validated_email)
                if valid_emails:
                    return valid_emails
        except Exception as e:
            print(f"Error fetching {link}: {e}")
    return valid_emails


def fetch_emails_from_url(url):
    """Attempt to fetch emails from a given URL."""
    valid_emails = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            emails = find_emails(response.text)
            for email in emails:
                validated_email = _validate_email(email)  # Validate each email
                if validated_email:  # If email is valid, add to the list
                    valid_emails.append(validated_email)
            if valid_emails:
                return valid_emails
            # If no valid emails found in the main page, check the contact page
            return find_emails_on_contact_page(response.text, url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return valid_emails

import pandas as pd
import random
import time

from website_scraper import find_business_website
from email_scraper import fetch_emails_from_url


def process_permits(csv_path, interim_output_csv):
    """Process permits CSV to find emails for each Permittee's Business Name and save progress."""
    df = pd.read_csv(csv_path)
    rows = df.shape[0]
    df["websites"] = ""
    df["emails"] = ""
    for index, row in df.iterrows():
        print(f"{((index + 1) / rows) * 100:.2f}%")
        business_name = row["Permittee's Business Name"]
        print(f"Processing: {business_name}")
        # Random delay of between 2 to 10 seconds
        time.sleep(random.randint(1, 10))
        websites = find_business_website(business_name)
        print("websites found: ", websites)
        df.at[index, "websites"] = ", ".join(websites)

        all_emails = []
        for website in websites:
            emails = fetch_emails_from_url(website)
            print("emails found: ", emails)
            if emails:
                all_emails.extend(emails)
        if all_emails:
            df.at[index, "emails"] = ", ".join(set(all_emails))

        print("**********************************************")

        # Save the DataFrame after each iteration to ensure progress is saved
        df.to_csv(interim_output_csv, index=False)

    return df


def save_results(df, output_csv):
    """Save the DataFrame with emails to a new CSV file."""
    df_to_save = df[
        [
            "Permittee's First Name",
            "Permittee's Last Name",
            "Permittee's Business Name",
            "emails",
            "websites",
        ]
    ]
    df_to_save.to_csv(output_csv, index=False)


def clean_emails():
    path = "output/MANHATTAN-emails-2024.csv"
    output_csv = "output/MANHATTAN-clean-emails-2024.csv"
    df = pd.read_csv(path)

    known_providers = {
        "gmail.com",
        "hotmail.com",
        "aol.com",
        "yahoo.com",
        "sbcglobal.net",
    }

    def is_email_valid(email, business_name):
        """Check if the email is valid based on the business name or is from a known provider."""
        email_domain = email.split("@")[-1].lower()
        business_name_parts = business_name.lower().split()

        # Check if the domain is a known provider
        if email_domain in known_providers:
            return True

        # Check if any part of the business name is in the email domain
        for part in business_name_parts:
            if part in email_domain:
                return True

        # If none of the conditions are met, the email is not considered valid
        return False

    for index, row in df.iterrows():
        business_name = row["Permittee's Business Name"]
        print(f"Processing: {business_name}")
        emails = row["emails"].split(", ") if pd.notnull(row["emails"]) else []
        valid_emails = []
        for email in emails:
            if is_email_valid(email, business_name):
                valid_emails.append(email)
        df.at[index, "emails"] = ", ".join(valid_emails)

    df.to_csv(output_csv, index=False)


def flatten_emails():
    path = "output/MANHATTAN-clean-emails-2024.csv"
    output_csv = "output/MANHATTAN-clean-and-flattened-emails-2024.csv"
    df = pd.read_csv(path)

    # Assuming the clean_emails function is already applied and 'emails' column is cleaned
    # Split the 'emails' column into a list of emails
    df["emails"] = df["emails"].apply(
        lambda x: x.split(", ") if isinstance(x, str) else []
    )

    # Explode the 'emails' column to have one email per row
    df = df.explode("emails")

    # Delete rows where 'emails' column is NaN or empty after the explode operation
    df = df.dropna(subset=["emails"])
    df = df[df["emails"] != ""]

    # Keep only the specified columns
    df = df[
        [
            "Permittee's First Name",
            "Permittee's Last Name",
            "Permittee's Business Name",
            "emails",
        ]
    ]

    # Save the flattened DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    csv_path = "output/deduped-MANHATTAN-permits-2024.csv"
    interim_output_csv = "output/MANHATTAN-emails-progress-2024.csv"
    output_csv = "output/MANHATTAN-emails-2024.csv"
    processed_df = process_permits(csv_path, interim_output_csv)
    save_results(processed_df, output_csv)
    # clean_emails()
    # flatten_emails()

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


if __name__ == "__main__":
    csv_path = "output/deduped-MANHATTAN-permits-2024.csv"
    interim_output_csv = "output/MANHATTAN-emails-progress-2024.csv"
    output_csv = "output/MANHATTAN-emails-2024.csv"
    processed_df = process_permits(csv_path, interim_output_csv)
    save_results(processed_df, output_csv)

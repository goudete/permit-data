import pandas as pd
from dateutil import parser


csv_file_path = "./city-data/DOB_Permit_Issuance_20240404.csv"
cols = [
    "Job #",
    "Filing Date",
    "Issuance Date",
    "Job Start Date",
    "DOBRunDate",
    "Permittee's First Name",
    "Permittee's Last Name",
    "Permittee's Phone #",
    "Owner's Business Type",
    "Owner's Business Name",
    "BOROUGH",
    "Permit Status",
    "Filing Status",
    "Permit Type",
]


def get_2024_permits():
    chunk_size = 10000
    filtered_rows = []
    rows = 3964133

    chunk_total = chunk_size

    for chunk in pd.read_csv(csv_file_path, usecols=cols, chunksize=chunk_size):
        print(f"{round((chunk_total/rows)*100, 2)}%")

        # Convert "Filing Date" to datetime using dateutil.parser.parse
        chunk["Filing Date"] = chunk["Filing Date"].apply(
            lambda x: (
                pd.NaT
                if pd.isna(x)
                else parser.parse(x, dayfirst=False, yearfirst=True, fuzzy=True)
            )
        )

        # Filter records where the year in "Filing Date" is 2024
        filtered_chunk = chunk[chunk["Filing Date"].dt.year == 2024]
        filtered_rows.append(filtered_chunk)
        chunk_total += chunk_size

    # Concatenate all filtered chunks
    df_2024 = pd.concat(filtered_rows)

    # Standardize "Permittee's Phone #" format to string and remove trailing '.0'
    df_2024["Permittee's Phone #"] = df_2024["Permittee's Phone #"].apply(
        lambda x: str(x).rstrip(".0") if pd.notna(x) else x
    )

    # Deduplicate based on "Permittee's Phone #"
    df_2024 = df_2024.drop_duplicates(subset=["Permittee's Phone #"])

    output_file_path = "ny-permits-2024.csv"
    df_2024.to_csv(output_file_path, index=False)

    print("outputted 2024 permit data with deduplication")


def search_for_job_number(job_number):
    df = pd.read_csv(csv_file_path)
    column_name = "Job #"

    # Find the row with the specified job number
    filtered_df = df[df[column_name] == job_number]

    if not filtered_df.empty:
        print(f"Row(s) with job number {job_number}:")
        print(filtered_df)

        output_file_path = f"${job_number}.csv"
        filtered_df.to_csv(output_file_path, index=False)
    else:
        print(f"No rows found with job number {job_number}.")


if __name__ == "__main__":
    project_id = input("Enter the job_number to filter by: ")
    if project_id:
        search_for_job_number(project_id)
    else:
        print("No project ID provided. Running 2024 permits retrieval.")
        get_2024_permits()

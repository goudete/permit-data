import pandas as pd
from dateutil import parser


csv_file_path = "./city-data/DOB_Permit_Issuance_20240404.csv"
cols = [
    "Job #",
    "Work Type",
    "Filing Date",
    "Issuance Date",
    "Job Start Date",
    "DOBRunDate",
    "House #",
    "Street Name",
    "Permittee's First Name",
    "Permittee's Last Name",
    "Permittee's Phone #",
    "Owner's Business Type",
    "Owner's Business Name",
    "BOROUGH",
    "Permit Status",
    "Filing Status",
    "Permit Type",
    "Permittee's Business Name",
]


def get_permits_by_year(year):
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
        filtered_chunk = chunk[chunk["Filing Date"].dt.year == int(year)]
        filtered_rows.append(filtered_chunk)
        chunk_total += chunk_size

    # Concatenate all filtered chunks
    df = pd.concat(filtered_rows)

    row_count = df.shape[0]
    print(f"Number of rows in df: {row_count}")
    output_file_path = f"ny-permits-${year}-with-business-name.csv"
    df.to_csv(output_file_path, index=False)

    print(f"outputted {year} permit data")


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


def dedupe():
    path = "./output/ny-permits-2024-with-business-name.csv"
    output_path = "./output/deduped-2024.csv"
    col = "Permittee's Business Name"

    df = pd.read_csv(path)
    deduped_df = df.drop_duplicates(subset=[col])

    deduped_df.to_csv(output_path, index=False)


def filter_by_borough(borough):
    df = pd.read_csv("./output/deduped-2024-permits.csv")
    filtered_df = df[df["BOROUGH"] == borough.upper()]

    # Save the filtered DataFrame to a new CSV file
    output_file_path = f"./output/deduped-{borough}-permits-2024.csv"
    filtered_df.to_csv(output_file_path, index=False)

    print(f"Filtered data saved to {output_file_path}")


if __name__ == "__main__":
    function_to_run = input("Enter the function you want to run: ")
    if function_to_run == "get_permits_by_year":
        year = input("Enter year to retrieve: ")
        get_permits_by_year(year)
    elif function_to_run == "search_for_job_number":
        job_number = input("Enter the job number to filter by: ")
        search_for_job_number(job_number)
    elif function_to_run == "dedupe":
        dedupe()
    elif function_to_run == "filter_by_borough":
        borough = input("Enter burough to filter by: ")
        filter_by_borough(borough)
    else:
        print("No matched function :(")

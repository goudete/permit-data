import pandas as pd


csv_file_path = "./city-data/SF_Planning_Permitting_Data_2024040.csv"


def get_via_project_id(project_id):
    df = pd.read_csv(csv_file_path)
    column_name = "RECORD_ID"

    filtered_df = df[df[column_name] == project_id]

    # Save the filtered row to a new CSV file
    output_file_path = f"{project_id}.csv"
    filtered_df.to_csv(output_file_path, index=False)

    print(f"Filtered row saved to {output_file_path}")


def get_ev_fleet_projects():
    df = pd.read_csv(csv_file_path)
    column_name = "OTHER_NON_RES_DESC"
    land_use = "EV"

    # Use str.contains to filter rows where the column contains the land_use string
    filtered_df = df[df[column_name].str.contains(land_use, na=False)]

    # Save the filtered rows to a new CSV file
    output_file_path = f"{land_use}.csv"
    filtered_df.to_csv(output_file_path, index=False)

    print(f"Filtered rows saved to {output_file_path}")


if __name__ == "__main__":
    project_id = input("Enter the project ID to filter by: ")
    if project_id:
        get_via_project_id(project_id)
    else:
        print("No project ID provided. Running EV fleet projects retrieval.")
        get_ev_fleet_projects()

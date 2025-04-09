import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

credentials_json ='proj2026-04689d6ef2c7.json'

def upload_csv_to_bigquery(dataframe):
    project_id = 'proj2026'
    dataset_id= 'streamlit'
    table_id = 'data'

    # Set up BigQuery client with service account credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_json)
    client = bigquery.Client(project=project_id, credentials=credentials)

    # Read the CSV file into a pandas DataFrame
    df = (dataframe)

    # Define the table reference
    table_ref = client.dataset(dataset_id).table(table_id)

    # Upload DataFrame to BigQuery
    df.to_gbq(destination_table=f"{dataset_id}.{table_id}",
              project_id=project_id,
              if_exists='replace',  # Options: 'fail', 'replace', 'append'
              credentials=credentials)

    print(f"Data uploaded successfully to BigQuery table: {table_ref}")

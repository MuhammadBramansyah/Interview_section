from ingest_data_to_gsheet import ingest_data_to_gsheet
from ingest_to_bq import send_to_bigquery

if __name__ == "__main__":
    ingest_data_to_gsheet()
    send_to_bigquery()
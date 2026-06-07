"""
Pulls Alzheimer's/Cognitive Decline data from the CDC's "Alzheimer's Disease and Healthy Aging Data" dataset.
Dataset: https://data.cdc.gov/resource/hfr9-rurv.json
Class filtered to: "Cognitive Decline"

"""
import requests
import pandas as pd
import time


BASE_URL   = "https://data.cdc.gov/resource/hfr9-rurv.json"
BATCH_SIZE = 1000   # CDC API max per request
OUTPUT     = "raw_alzheimers.csv"

# We only want the Cognitive Decline class (most relevant to Alzheimer's)
WHERE_FILTER = "class='Cognitive Decline'"


def fetch_all_records():
    all_records = []
    offset = 0

    while True:
        params = {
            "$where":  WHERE_FILTER,
            "$limit":  BATCH_SIZE,
            "$offset": offset, # Where to start reading from
            "$order":  "yearstart DESC"
        }

        response = requests.get(BASE_URL, params=params, timeout=30)

        # Stop if the server returns an error based on HTTP status code
        # If 200 = OK, 400 = Bad request, 403 = Forbidden, 404 = Not found, 500 = Server error
        if response.status_code != 200: 
            print(f"Error {response.status_code}: {response.text}")
            break

        batch = response.json() # Converts raw response into Python list of dictionaries

        if not batch:
            break  # No more data, API returning empty list

        all_records.extend(batch)
        print(f"etched {len(all_records)} records.")

        if len(batch) < BATCH_SIZE: 
            break  # Last page since if we asked for 1000 rows and only got 743 that means we've hit last page.

        offset += BATCH_SIZE # Progresses starting position for loop by batch size.
        time.sleep(0.3)  # Pausing API pull request so CDC server don't see as spam and block you.

    return all_records

def main():
    records = fetch_all_records()

    if not records:
        print("No records found.")
        return

    df = pd.DataFrame(records)

    print(f"\nTotal records fetched: {len(df)}")
    print(f"Columns: {list(df.columns)}\n")

    # Save raw data
    df.to_csv(OUTPUT, index=False)
    print(f"Raw data saved to: {OUTPUT}")

if __name__ == "__main__":
    main()
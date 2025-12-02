import pandas as pd
from pymongo import MongoClient
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGODB_URL = os.environ.get("MONGODB_URL")


class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = MongoClient(MONGODB_URL)
            logging.info("MongoDB connection established successfully")
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def csv_to_json(self, file_path):
        """
        Reads a CSV file and converts it to a list of JSON/dict records.
        """
        try:
            logging.info(f"Reading data from: {file_path}")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"CSV file does not exist: {file_path}")

            data = pd.read_csv(file_path)
            data = data.reset_index(drop=True)
            records = data.to_dict(orient="records")

            logging.info(f"Records created successfully: {len(records)} records")
            return records

        except Exception as e:
            logging.error(f"Error reading CSV: {e}")
            raise NetworkSecurityException(e, sys.exc_info())

    def insert_data_mongodb(self, records, database, collections):
        """
        Inserts a list of JSON records into MongoDB.
        """
        try:
            db = self.mongo_client[database]
            coll = db[collections]
            result = coll.insert_many(records)
            logging.info(f"Inserted {len(result.inserted_ids)} records into {database}.{collections}")
            return result.inserted_ids

        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {e}")
            raise NetworkSecurityException(e, sys.exc_info())

    def read_data_mongodb(self, database, collections, query={}):
        """
        Reads data from MongoDB collection.
        query: optional MongoDB filter (default = all documents)
        Returns: list of dicts (records)
        """
        try:
            db = self.mongo_client[database]
            coll = db[collections]
            data = list(coll.find(query, {"_id": 0}))
            logging.info(f"Read {len(data)} records from {database}.{collections}")
            return data
        except Exception as e:
            logging.error(f"Error reading data from MongoDB: {e}")
            raise NetworkSecurityException(e, sys.exc_info())


if __name__ == "__main__":
    try:
        extractor = NetworkDataExtract()

        # CSV file relative path
        csv_file = "data/phisingData.csv"

        # Convert CSV to JSON
        records = extractor.csv_to_json(csv_file)

        # Insert data into MongoDB
        inserted_ids = extractor.insert_data_mongodb(records, "networksecuritydata", "data")
        logging.info(f"Inserted IDs: {inserted_ids[:5]} ...")  # Show first 5 IDs

        # Read data from MongoDB
        data_from_db = extractor.read_data_mongodb("networksecuritydata", "data")
        logging.info(f"First 5 records from MongoDB:\n{data_from_db[:5]}")

    except NetworkSecurityException as e:
        logging.error(f"NetworkSecurityException occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

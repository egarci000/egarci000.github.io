import os
from pymongo import MongoClient


class CRUD:

    def __init__(self,
                 username=None,
                 password=None,
                 db_name="coursesDB",
                 collection_name="courses",
                 host="localhost",
                 port=27017):
        try:
            # Checks if MONGO_URI environment variable is set
            mongo_uri = os.getenv("MONGO_URI")

            if mongo_uri:
                print(
                    "Using MongoDB Atlas connection from environment variable."
                )
                self.client = MongoClient(mongo_uri)
            else:
                # Fallback for local MongoDB setup
                print("Using local MongoDB connection.")
                uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
                self.client = MongoClient(uri)

            # Select database and collection
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]

            # Ensure an index on course_number for faster lookups
            self.collection.create_index("course_number", unique=True)
            print("MongoDB connection established successfully!")

        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None

    def create(self, document):
        """Insert a document into the collection."""
        try:
            result = self.collection.insert_one(document)
            return result.inserted_id is not None
        except Exception as e:
            print(f"Couldn't insert: {e}")
            return False

    def read(self, query):
        """Find documents that match a given query."""
        try:
            return list(self.collection.find(query))
        except Exception as e:
            print(f"Error reading documents: {e}")
            return []

    def update(self, query, new_data):
        """Update documents in the collection."""
        try:
            result = self.collection.update_many(query, {"$set": new_data})
            return result.modified_count
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete(self, query):
        """Delete documents that match a given query."""
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0

    def delete_all(self):
        """Deletes all documents in the current collection."""
        result = self.collection.delete_many({})
        print(
            f"Deleted {result.deleted_count} existing document(s) from MongoDB."
        )

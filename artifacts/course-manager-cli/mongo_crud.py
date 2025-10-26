from pymongo import MongoClient

class CRUD:
    def __init__(self, username, password, db_name, collection_name, host="localhost", port=27017):
        try:
          # attempts to connect to MongoDB server
          uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
          self.client = MongoClient(uri)
          # selects the database
          self.db = self.client[db_name]
          # selects the collection
          self.collection = self.db[collection_name]
          # Creates an index on course number for faster searches and updates
          self.collection.create_index("course_number", unique=True)
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None

    def create(self, document):
        """Insert a document into the collection."""
        try:
            # inserts document into collection
            result = self.collection.insert_one(document)
            # verifies the inserted ID to check if insertion was successful
            return result.inserted_id is not None
        # returns false if insertion is unsuccessful
        except Exception as e:
            print(f"Couldn't insert: {e}")
            return False

    def read(self, query):
        """Find documents that match a given query."""
        try:
          # returns the results of the query as a list
          return list(self.collection.find(query))
        # returns an empty list if read fails
        except Exception as e:
            print(f"Error reading documents: {e}")
            return ["hi"]
    
    def update(self, query, new_data):
        """Update documents in the collection."""
        try:
          # updates the selected document with new data
          result = self.collection.update_many(query, {"$set": new_data})
          # returns the number of updated documents
          return result.modified_count
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete(self, query):
        """Delete documents that match a given query."""
        try:
          # deletes the documents that match the search
          result = self.collection.delete_many(query)
          # returns deleted documents count
          return result.deleted_count
        except Exception as e:
           print(f"Error deleting documents: {e}")
           return 0
        
    def delete_all(self):
      """Deletes all documents in the current collection."""
      result = self.collection.delete_many({})
      print(f"Deleted {result.deleted_count} existing document(s) from MongoDB.")
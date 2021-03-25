from pymongo import MongoClient
import pymongo


class MongoDB:
    def __init__(self, database_name, uri):
        self.client = MongoClient(uri)
        self.database = self.client[database_name]

    @staticmethod
    def find_dictionary(programming, query):
        return programming.find(query)

    def find_one(self, collection, query):
        return self.database[collection].find_one(query)

    def find_one_lasted(self, collection, query):
        return self.database[collection].find_one(query, sort=[('_id', pymongo.DESCENDING)])

    def find(self, collection, query):
        return self.database[collection].find(query)

    def insert_one(self, collection, data):
        ids = None
        try:
            result = self.database[collection].insert_one(data)
            ids = result.inserted_ids
        except Exception as e:
            print(str(e))
        return ids

    def insert_many(self, collection, data):
        ids = None
        try:
            result = self.database[collection].insert_many(data)
            ids = result.inserted_ids
        except Exception as e:
            print(str(e))
        return ids

    def update_many(self, collection, query, values):
        try:
            self.database[collection].update_many(query, values)
        except Exception as e:
            print(str(e))

    def update_one(self, collection, query, values):
        try:
            self.database[collection].update_one(query, values)
        except Exception as e:
            print(str(e))

    def delete_one(self, collection, query):
        try:
            self.database[collection].delete_one(query)
        except Exception as e:
            print(str(e))

    def delete_many(self, collection, query):
        try:
            self.database[collection].delete_many(query)
        except Exception as e:
            print(str(e))

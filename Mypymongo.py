import pymongo
from pymongo import MongoClient


class Mydb:
    def __init__(self):
        self.cluster = MongoClient(
            "Your mongo key")
        self.db = self.cluster["Client_database"]
        self.collection = self.db["Client_collection"]
        self.id = self.collection.find({"_id": 0})[0]["id_count"]
        self.this = None
        ### when user login, this will change like self.this = self.find({"username": username})[0]

    def find(self, target):     # dict
        results = self.collection.find(target)
        temp_list = [x for x in results]
        return temp_list        # return list

    def insert(self, target, many=True):       # list, list contain dict
        if many:
            self.collection.insert_many(target)
        else:
            self.collection.insert_one(target)

    def delete(self, target, many=True):       # dict
        if many:
            self.collection.delete_many(target)
        else:
            self.collection.delete_one(target)

    def update(self, target, value, many=True):       # dict, dict
        if many:
            self.collection.update_many(target, {"$set": value})
        else:
            self.collection.update_one(target, {"$set": value})

    def append_history(self, value):        # dict, list
        tmp = [x for x in self.this["history"]]
        if len(tmp) >= 5:
            tmp = tmp[1:]
        tmp.append(value)
        self.collection.update_one({"_id": self.this["_id"]}, {"$set": {"history": tmp}})
        self.this = self.find({"_id": self.this["_id"]})[0]

    def show_history(self):
        return db.this["history"]

if __name__ == "__main__":
    db = Mydb()
    # under line will append to success sign in
    db.this = db.find({"username": "Yuli"})[0]
    # under line will append to success sign up
    # db.update({"_id": db.this["_id"]}, {"history": []})
    print(db.show_history())
    # under line will append to search
    db.append_history(["Time", "BE"])
    # db.show_history() will return [ ["Book name", "Book store"], ["Python", "LBEK"] ]
    print(db.show_history())

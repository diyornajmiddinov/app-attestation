import uuid

import pymongo
from bson import ObjectId


class Database:
    def __init__(self) -> None:
        self.url = "mongodb://localhost:27017"
        self.client = pymongo.MongoClient(self.url)
        self.mydb = self.client["app-attestatsiya"]
        self.users = self.mydb["users"]
        self.channels = self.mydb["channels"]
        self.tests = self.mydb["tests"]
        self.subject = self.mydb["subject"]
        self.test_number = self.mydb["test_number"]
        self.subject_tests = self.mydb["subject_tests"]

    def find_user(self, user_id: int):
        return self.users.find_one({'_id': user_id})

    def add_user(self, user_id: int, name: str):
        is_admin = False
        if user_id == 5351489385:
            is_admin = True
        query = {"_id": user_id, "name": None, "is_admin": is_admin}
        self.users.insert_one(query)

    def find_all_users(self):
        return self.users.find({})

    def find_admins(self):
        return self.users.find({"is_admin": True})

    def add_admin(self, user_id: int):
        old = {"_id": user_id}
        new = {"$set": {"is_admin": True}}
        self.users.update_one(old, new)

    def remove_admin(self, user_id: int):
        old = {"_id": user_id}
        new = {"$set": {"is_admin": False}}
        self.users.update_one(old, new)

    def delete_user(self, user_id: int):
        self.users.delete_one({'_id': user_id})

    # -------------------------------------------
    # -------------------------------------------
    # -------------------------------------------

    def find_channel(self, channel_id: int):
        return self.channels.find_one({'_id': channel_id})

    def find_all_channels(self):
        return self.channels.find({})

    def add_channel(self, channel_id: int, link: str):
        query = {"_id": channel_id, "link": link}
        self.channels.insert_one(query)

    def delete_channel(self, channel_id: int):
        self.channels.delete_one({'_id': channel_id})

    # -------------------------------------------
    # -------------------------------------------
    # -------------------------------------------

    def add_test(self, test_id: str, test: str, question: str, photo_id: str = None):
        test_number = self.test_number.find_one({"_id": 1})
        if test_number is None:
            self.test_number.insert_one({"_id": 1, "number": 1})
            test_number = self.test_number.find_one({"_id": 1})
        number = int(test_number.get("number"))
        self.tests.insert_one(
            {
                "_id": test_id,
                "test": test,
                "test_number": number,
                "question": question,
                "photo_id": photo_id,
                "a": None,
                "b": None,
                "c": None,
                "d": None,
                "answer": None
            }
        )
        self.test_number.update_one({"_id": 1}, {"$set": {"number": number + 1}})

    def update_test(self, test_id: str, answer: str, result: str):
        self.tests.update_one({"_id": test_id}, {"$set": {answer: result}})

    def find_test(self, test_id: str):
        return self.tests.find_one({"_id": test_id})

    def restart_test(self):
        self.test_number.update_one({"_id": 1}, {"$set": {"number": 1}})

    # -------------------------------------------
    # -------------------------------------------
    # -------------------------------------------

    def add_subject(self, _id: str, name: str):
        self.subject.insert_one({"_id": _id, "name": name})

    def find_all_subjects(self):
        return self.subject.find({})

    # -------------------------------------------
    # -------------------------------------------
    # -------------------------------------------

    def add_subject_test(self, _id: str, name: str, subject_id:str):
        self.subject.insert_one({"_id": _id, "name": name, "subject_id": subject_id})

    def find_all_subject_tests(self,subject_id:str):
        return self.subject.find({"subject_id":subject_id})

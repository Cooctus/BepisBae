from datetime import datetime, timedelta
from os import environ

from pymongo import MongoClient


class DatabaseConnection:

  def __init__(self):
    self.connection = MongoClient()
    self.db = self.connection['BepisBot']
    self.profiles = self.db.profiles
    self.profiles.create_index("user_id", unique=True)

  def add_user(self, user_id: str, username: str):
    prof = {
      "user_id": user_id,
      "username": username,
      "bepis" : 0,
      "inventory": {
       "Shibes": {
          "name": {},
          "happ": 100
        }
      },
      "invites": {}

    }
    self.profiles.insert_one(prof)
    return prof

  def find_user(self, user_id: str):
    user = self.profiles.find_one({"user_id": user_id})
    if not user:
      return None
    return user

  def change_bepis(self, user_id, amount: int):
    self.profiles.update_one({"user_id": user_id}, {"$set": {"bepis": amount}})

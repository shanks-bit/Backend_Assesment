# one user 
from models.user import PostModel


def DecodeUser(doc) -> dict:
    return {
        "_id" : str(doc["_id"]) ,
        "user_id": doc["user_id"] ,
        "name": doc["name"] ,
        "mobile_no": doc["mobile_no"] ,
        "email": doc["email"] ,
        "posts": doc["posts"] ,
        "date" : doc["date"] ,
    }

# all users 
def DecodeUsers(docs) -> list:
    return [DecodeUser(doc) for doc in docs]
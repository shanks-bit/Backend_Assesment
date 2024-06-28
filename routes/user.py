from typing import List
from fastapi import APIRouter, HTTPException, Query
from models.user import UserModel, UpdateUserModel, PostModel, UpdatePostModel
from config.config import users_collection
import datetime
from bson import ObjectId
import bson
from serializers.user import DecodeUser, DecodeUsers

user_root = APIRouter()

# post request for Users
@user_root.post("/new/user")
async def NewUser(doc:UserModel):
    doc = dict(doc)

    if doc.get("posts"):
        doc["posts"] = [post.dict() for post in doc["posts"]]
    current_date = datetime.date.today()
    doc["date"] = str(current_date)
    
    res = users_collection.insert_one(doc)

    doc_id = str(res.inserted_id)

    return {
        "status" : "ok" ,
        "message" : "Blog posted successfully" , 
        "_id" : doc_id
    }


# get all users
@user_root.get("/all/users")
async def AllUsers():
    res =  users_collection.find() 
    decoded_data = DecodeUsers(res)

    return {
        "status": "ok" , 
        "data" : decoded_data
    }


# get user by name
@user_root.get("/users/{name}")
async def GetUser(name: str) :
    res = users_collection.find_one({"name" : name})
    decoded_user = DecodeUser(res)
    return {
        "status" : "ok" ,
        "data" : decoded_user
    }


# get  single post for a user
@user_root.get("/posts/search/")
async def search_posts_by_hashtag(hashtags: List[str] = Query(...)):
    users = users_collection.find({"posts.hashtags": {"$in": hashtags}})
    matching_posts = []
    for user in users:
        for post in user.get("posts", []):
            if any(hashtag in post["hashtags"] for hashtag in hashtags):
                matching_posts.append(post)
    return matching_posts


# post request for Posts
@user_root.post("/new/user/{user_id}/post")
async def add_post(user_id: str, post: PostModel):
    post_dict = dict(post)
    update_result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$push": {"posts": post_dict}})
    if update_result.modified_count:
        return {
            "status": "ok",
            "message": "Post added successfully"
        }
    raise HTTPException(status_code=404, detail="User not found")


# update user
@user_root.patch("/update/{user_id}")
async def UpdateUser(user_id: str , doc:UpdateUserModel):
    req = dict(doc.model_dump(exclude_unset=True)) 
    update_result = users_collection.find_one_and_update(
       {"_id" : ObjectId(user_id) } ,
       {"$set" : req}
    )

    return {
        "status" : "ok" ,
        "message" : "user updated successfully"
    }


# update users post
@user_root.patch("/update/{user_id}/post/post_id")
async def UpdateUserPost(user_id: str, post_id: int, doc:UpdatePostModel):

    post_dict = dict(doc.model_dump(exclude_unset=True))
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        for idx, existing_post in enumerate(user.get("posts", [])):
            if existing_post["post_id"] == post_id:
                user["posts"][idx] = post_dict
                update_result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"posts": user["posts"]}})
                if update_result.modified_count:
                    return {
                        "status": "ok",
                        "message": "Post updated successfully"
                    }
        raise HTTPException(status_code=404, detail="Post not found")
    raise HTTPException(status_code=404, detail="User not found")


# delete a user
@user_root.delete("/delete/{user_id}")
async def  deleteUser(user_id : str):
    users_collection.find_one_and_delete(
        {"_id" : ObjectId(user_id)}
    )

    return {
        "status" : "ok" ,
        "message" : "User deleted succesfully"
    }


# delete a post
@user_root.delete("/user/{user_id}/post/{post_id}")
async def deletePost(user_id: str, post_id: int):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        posts = user.get("posts", [])
        posts = [post for post in posts if post["post_id"] != post_id]
        update_result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"posts": posts}})
        if update_result.modified_count:
            return {
                "status": "ok",
                "message": "Post deleted successfully"
            }
        raise HTTPException(status_code=404, detail="Post not found")
    raise HTTPException(status_code=404, detail="User not found")

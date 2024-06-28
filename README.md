# Backend_Assesment

This is a simple CRUD project made in python language using FAST API framework and Mongo DB database.

In this project users can be created and those users can post discussions and using them simple operations

are performed.



Project Structure follows----


---config
   ---config.py

   
---models
   ---user.py

   
---routes
   ---user.py

   
---serializers
   ---user.py

   
---main.py


config -It has mongo db connection code and the database.

models - It has models created according to which user can insert data in database.

routes - It has all the endpoints created for user and posts

serializers - During GET requect from the database data havr to be seriealized.

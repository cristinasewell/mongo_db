import pymongo
import datetime


# create a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# define the travel_db database in Mongo
db = client.travel_db

# quering all destinations
dest = db.destinations.find()

for d in dest:
    print(d)


# inserting a document into the destination collection
db.destinations.insert_one(
    {
        "continent": "Europe",
        "country": "Moldova",
        "major_cities": ["Chisinau", "Stefan-Voda", "Causeni"]
    }
)

# updating a document - adding an item to a document array
# db.destinations.update_one(
#     {
#         "country": "Moldova"
#     },
#     {"$push": 
#         {"major_cities": "Antonesti"}
#     }
# )

# # deleting a field from document
# db.destinations.update_one(
#     {"country": "Moldova"},
#     {"$unset":
#         {"major_cities": ""}
#     }
#     )


# deleting a document from a collection
# db.destinations.delete_one(
#     {
#         "country": "Moldova"
#     }
# )

# A dictionary that represents the document to be inserted
post = {
    "continent": "Europe",
    "country": "Romania",
    "major_cities": ["Bucuresti", "Cluj-Napoca", 'Iasi', 'Timisoara'],
    "date": datetime.datetime.utcnow()
}
# Insert the document into the database
# The database and collection, if they don't already exist, will be created at this point.
db.destinations.insert_one(post)
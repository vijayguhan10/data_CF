# import pymongo

# client = pymongo.MongoClient('mongodb://localhost:27017/')
# database = client['videosoftware']
# collection = database['fs.files']  # Replace 'your_collection_name' with the actual name of your collection

# product = collection.find_one({"Date": "05-04-2024"})
# if product:
#     for key in product:
#         print(key, ":", product[key])
# else:
print("No document found for the given date.")

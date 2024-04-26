from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['facesoftware']  
collection = db['fs.files']  

def get_video_filenames_by_date(date):
    files = collection.find({"metadata.Date": date})

    filenames = []
    for file in files:
        filenames.append(file["filename"])

    return filenames

date = '25-04-2024'  
video_filenames = get_video_filenames_by_date(date)
for filename in video_filenames:
    print(filename)

from pymongo import MongoClient
from gridfs import GridFS
import subprocess
import pytz
import datetime

ist = pytz.timezone('Asia/Kolkata')

# Establish connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Accessing the database
db = client['your_database_name']

# Initialize GridFS for video storage
fs = GridFS(db)

def read_file(title, filename, fs):
    # Get current time in IST
    new_time = datetime.datetime.now(ist).strftime("%I:%M:%S")
    h = datetime.datetime.now(ist).strftime("%H")

    with open(filename, 'rb') as video_file:
        saving_detail = {
            "Time": new_time,
            "Hour": h
        }
        video_id = fs.put(video_file, filename=title, metadata=saving_detail)
        print('New video ID:', video_id)

# Inserting the video file into MongoDB using GridFS
read_file('My Video', 'D:/DATACFNEW/saved_videos/Face recognition (1).mp4', fs)

def retrieve_and_convert_to_mp4(video_name):
    # Find the video in GridFS
    video_file = fs.find_one({"filename": video_name})

    if video_file:
        # Retrieve the video content
        video_content = video_file.read()

        # Define the input file path
        input_file_path = f'{video_name}.tmp'

        # Write the content to a temporary file
        with open(input_file_path, 'wb') as temp_file:
            temp_file.write(video_content)

        # Define the output file path for the converted MP4 file
        output_file_path = f'{video_name}.mp4'

        # Convert the video to MP4 format using ffmpeg
        completed_process = subprocess.run(['ffmpeg', '-i', input_file_path, output_file_path])

        # Check if the conversion was completed successfully
        if completed_process.returncode == 0:
            print("Video conversion completed successfully.")
        else:
            print("Video conversion failed.")
    else:
        print("Video not found.")

# Example usage:
# Retrieve and convert the video to MP4
retrieve_and_convert_to_mp4('My Video')

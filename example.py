import pymongo
import gridfs
import pytz
import datetime
import subprocess
client = pymongo.MongoClient('mongodb://localhost:27017/')
ist = pytz.timezone('Asia/Kolkata')

def read_file(title, filename, fs):
    with open(filename, 'rb') as video_file:
        new_time = datetime.datetime.now(ist).strftime("%I:%M:%S")
        hour = datetime.datetime.now(ist).strftime("%H")
        saving_detail = {"Time": new_time, "Hour": hour}
        video_id = fs.put(video_file, title=title, metadata=saving_detail)
        print('New video ID:', video_id)

db = client['videodata']
fs = gridfs.GridFS(db)
read_file('My Video', 'D:/DATACFNEW/saved_videos/Face recognition (1).mp4', fs)

def retrieve_and_convert_to_mp4(video_name, fs):
    video_file = fs.find_one({"filename": video_name})
    if video_file:
        video_content = video_file.read()
        input_file_path = f'{video_name}.tmp'
        with open(input_file_path, 'wb') as temp_file:
            temp_file.write(video_content)
        output_file_path = f'{video_name}.mp4'
        ffmpeg_path = 'D:/datacf_path/ffmpeg'
        completed_process = subprocess.run([ffmpeg_path, '-i', input_file_path, output_file_path])
        if completed_process.returncode == 0:
            print("Video conversion completed successfully.")
        else:
            print("Video conversion failed.")
    else:
        print("Video not found.")

retrieve_and_convert_to_mp4('My Video', fs)

client.close()

from flask import Flask, render_template, send_from_directory, request
import gridfs
import subprocess
from datetime import datetime
import pymongo
import os

client = pymongo.MongoClient('mongodb://localhost:27017/')
database = client['facesoftware']
datamanagement = gridfs.GridFS(database)

app = Flask(__name__)

VIDEO_DIRECTORY = 'videos'

@app.route('/')
def index():
    return render_template('face.html')

@app.route('/FORMDETAILS', methods=['POST'])
def form_details():
    if request.method == 'POST':
        datepassed = request.form['datepassed']
        date_object = datetime.strptime(datepassed, '%Y-%m-%d')
        formatted_date = date_object.strftime('%d-%m-%Y')

        def get_video_filenames_by_date(date):
            files = database.fs.files.find({"metadata.Date": date})
            filenames = [file["filename"] for file in files]
            return filenames

        video_filenames = get_video_filenames_by_date(formatted_date)
        for filename in video_filenames:
            print(filename)
            retrieve_and_convert_to_mp4(filename, datamanagement)

        return render_template('face.html', video_filenames=video_filenames)

@app.route('/video/<path:filename>')
def serve_video(filename):
    video_path = os.path.join(VIDEO_DIRECTORY, filename + '.mp4')
    if os.path.exists(video_path):
        return send_from_directory(VIDEO_DIRECTORY, filename + '.mp4')
    else:
        return 'Video not found', 404

def retrieve_and_convert_to_mp4(video_name, fs):
    video_file = fs.find_one({"filename": video_name})
    if video_file:
        video_content = video_file.read()
        input_file_path = os.path.join(VIDEO_DIRECTORY, f'{video_name}.tmp')
        with open(input_file_path, 'wb') as temp_file:
            temp_file.write(video_content)
        output_file_path = os.path.join(VIDEO_DIRECTORY, f'{video_name}.mp4')
        ffmpeg_path = 'D:/datacf_path/ffmpeg'  
        completed_process = subprocess.run([ffmpeg_path, '-i', input_file_path, output_file_path])
        if completed_process.returncode == 0:
            print("Video conversion completed successfully.")
        else:
            print("Video conversion failed.")
    else:
        print("Video not found.")

if __name__ == "__main__":
    if not os.path.exists(VIDEO_DIRECTORY):
        os.makedirs(VIDEO_DIRECTORY)
    app.run(debug=True)

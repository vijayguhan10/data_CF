import cv2
import os
import pymongo
import gridfs
import pytz
import datetime
import subprocess
import threading

client = pymongo.MongoClient('mongodb://localhost:27017/')
database = client['facesoftware']
datamanagement = gridfs.GridFS(database)

def videorecordingsave(filename, fs, title,video_count):
    with open(filename, 'rb') as videofile:
        saving_detail = {
            "Date": datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y"),
            "Time": datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%I:%M:%S"),
            "Title": title,
            "video_count": video_count 
        }
        videoid = fs.put(videofile, filename=title, metadata=saving_detail)
        print('Video saved as binary in MongoDB:', videoid)

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
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
        print("vide not found.")

def detect_faces_and_record():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    face_shake_count = 0
    save_dir = 'saved_videos'
    create_directory(save_dir)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    save_path = os.path.join(save_dir, 'saved_video.mp4')
    out = cv2.VideoWriter(save_path, fourcc, 20.0, (640, 480))

    video_count_doc = database.metadata.find_one({"key": "video_count"})
    if video_count_doc:
        video_count = video_count_doc["value"]
    else:
        video_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame")
            cv2.putText(frame, "No source", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) == 0:
                cv2.putText(frame, "No face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                out.write(frame)
                                                                    
                if face_shake_count >= 10:
                    print(f"Video saved: {save_path}")
                    face_shake_count = 0

                else:
                    face_shake_count += 1

        cv2.imshow('Face Recognition', frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    videorecordingsave(save_path, datamanagement, f'newvideosized{video_count}',video_count)

    retrieve_and_convert_to_mp4(f'newvideosized{video_count}', datamanagement)

record_thread = threading.Thread(target=detect_faces_and_record)
record_thread.start()

database.metadata.update_one({"key": "video_count"}, {"$inc": {"value": 1}}, upsert=True)

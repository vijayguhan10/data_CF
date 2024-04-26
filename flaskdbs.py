from flask import Flask, render_template
import pymongo
import datetime
import pytz

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['CarCollection']
collection = db['Cars']

ist = pytz.timezone('Asia/Kolkata')

# Get the current date and time in Indian time
formatted_time = datetime.datetime.now(ist).strftime('%I:%M:%S %p')

# Insert new car details into the MongoDB collection
new_car = {
    "brand": "Toyota",
    "model": "Camry",
    "color": "Silver",
    "year": 2022,
    "datetime": formatted_time
}
collection.insert_one(new_car)

@app.route('/')
def returndata():
    car_data = list(collection.find({},{"name":1,"_id":0}))
    print(car_data)
    return render_template('mongodb.html', data=car_data, current_datetime=formatted_time)

if __name__ == "__main__":
    app.run(debug=True)

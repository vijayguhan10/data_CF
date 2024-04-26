import requests

def get_address(latitude, longitude):
    api_key = 'AIzaSyAjlF-JfPsAvsvyDqnqMyqvrKmqAOJq81M'
    
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['formatted_address']
    else:
        return "Address not found"

def main():
    latitude = 11.6643
    longitude = 78.1460

    print("Latitude:", latitude)
    print("Longitude:", longitude)

    address = get_address(latitude, longitude)
    print("Address:", address)

if __name__ == "__main__":
    main()

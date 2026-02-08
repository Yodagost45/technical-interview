import nmea_parser
import vehicle_upload
import requests
import pandas as pd

#ask for user input of file name for output csv and nmea file
def main():
    

    #ask for vehicle reg
    #check api for list of existing vehicles
    #If vehicle exists, ask for confirmation "Edit existing vehicle? (y/n)"
    #If yes, skip creating vehicle
    #If no, create vehicle
    
    get_vehicles_request = requests.get("http://127.0.0.1:8000/vehicles")
    print("Vehicle list:")
    for vehicle in get_vehicles_request.json():
        print(vehicle)
    print("Enter vehicle number plate:")
    input_number_plate = input()
    vehicle_exists_already = False
    for vehicle in get_vehicles_request.json():
        if input_number_plate == vehicle["number_plate"]:
            vehicle_exists_already = True
            vehicleID = vehicle["id"]


    edit_vehicle = False
    create_vehicle = False

    if vehicle_exists_already:
        
        edit_vehicle = get_y_n_input("Edit existing vehicle?")
    else:
        create_vehicle = get_y_n_input("Create new vehicle?")
    
    if create_vehicle:
        print(input_number_plate)
        payload = {'number_plate': input_number_plate}
        create_vehicle_request = requests.post('http://127.0.0.1:8000/vehicles', json=payload)
        
        if not test_request(create_vehicle_request):
            return
        vehicleID = create_vehicle_request.json()['id']
        print(vehicleID)

    if edit_vehicle or create_vehicle:
        #After above comments
        add_vehicle_data = get_y_n_input("Add data to vehicle? (y/n)")
        
        if add_vehicle_data:
            print("Enter your nmea filename:")
            nmea_filename = input()
            print("Enter your csv filename:")
            csv_filename = input()
            if not csv_filename.endswith(".csv"):
                csv_filename += ".csv"
            nmea_parser.parse_file(nmea_filename=nmea_filename, output_csv_filename=csv_filename)
            post_csv(vehicleID, csv_filename)

def post_csv(vehicleID, csv_filename):
    df = pd.read_csv(csv_filename)
    print("post csv:")
    print(df)
    print("line by line:")
    
    for index, row in df.iterrows():
        print(row['lat'], row['lon'], row['hae'], row['timestamp'])
        payload = {
            "lat": row['lat'],
            "lon": row['lon'],
            "hae": row['hae'],
            "timestamp": row['timestamp']
        }
        link = 'http://127.0.0.1:8000/vehicles/' + str(vehicleID) + "/locations"
        create_location_request = requests.post(link, json=payload)
        
        #test if request was success
        if not test_request(create_location_request):
            return

        
    #Show list of locations uploaded
    print("############################ LOCATIONS UPLOADED #####################################")
    
    link = 'http://127.0.0.1:8000/vehicles/' + str(vehicleID) + "/locations"
    get_locations_request = requests.get(link)
    
    #test if request was success
    if not test_request(get_locations_request):
        return
    
    print(get_locations_request.json())


def test_request(request):
    if request.status_code == requests.codes.ok:
        return True
    request.raise_for_status()
    return False

def get_y_n_input(message):
    if not message.endswith(" (y/n)"):
        message +=  " (y/n)"
    while True:
        print(message)
        data = input()
        if data == "n" or data == "N" or data == "No" or data == "NO" or data == "no":
            output = False
            return output
        elif data == "y" or data == "Y" or data == "Yes" or data == "YES" or data == "yes":
            output = True
            return output
        print("Invalid input, try again")


# CODE STARTS HERE ------------------------------------------------------------------------
running = False
if __name__ == "__main__":
    running = True
while running:
    main()
    running = get_y_n_input("Add or edit another vehicle?")

    #Add check for if the server is not running
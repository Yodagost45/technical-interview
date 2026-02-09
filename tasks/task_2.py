import requests
from task_1 import get_y_n_input, test_request, print_vehicle_list

def check_vehicle_exists(get_vehicles_request, vehicle_id):
    for vehicle in get_vehicles_request.json():
        if vehicle_id == vehicle["id"]:
            print(vehicle)
            return True
    return False

def get_and_print_average_speed(vehicle_id):
    link = 'http://127.0.0.1:8000/vehicles/' + str(vehicle_id) + "/speed"
    get_speed_request = requests.get(link)
    
    test_request(get_speed_request)

    print("Average speed of vehicle with ID == " + str(vehicle_id) + ": " + str(get_speed_request.text).replace('"', '') )


# CODE STARTS HERE ------------------------------------------------------------------------
running = True
while(running):
    get_vehicles_request = print_vehicle_list()

    print("Get average speed of vehicle: (Enter id)")
    vehicle_id = int(input())

    if check_vehicle_exists(get_vehicles_request, vehicle_id):
        #Vehicle exists
        get_and_print_average_speed(vehicle_id)
    else:
        print("Error 404: Vehicle not found.")

    running = get_y_n_input("Calculate more speed?")

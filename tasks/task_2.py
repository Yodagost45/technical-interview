import requests
from task_1 import get_y_n_input, test_request

running = True
while(running):
    print("this is task 2")
    get_vehicles_request = requests.get("http://127.0.0.1:8000/vehicles")
    print("Vehicle list:")
    for vehicle in get_vehicles_request.json():
        print(vehicle)

    
    print("Get average speed of vehicle: (Enter id)")
    vehicle_id = int(input())

    vehicle_found = False

    for vehicle in get_vehicles_request.json():
        
        if vehicle_id == vehicle["id"]:
            vehicle_found = True
            print(vehicle)

    if vehicle_found:
        link = 'http://127.0.0.1:8000/vehicles/' + str(vehicle_id) + "/speed"
        get_speed_request = requests.get(link)

        #test if request was success
        if not test_request(get_speed_request):
            break
        print("Average speed of vehicle with ID == " + str(vehicle_id) + ": " + str(get_speed_request.text).replace('"', '') )
    else:
        print("Error 404: Vehicle not found.")

    running = get_y_n_input("Calculate more speed?")
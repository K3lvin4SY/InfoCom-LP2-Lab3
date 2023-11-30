import requests
import argparse
import time

#Write you own function that moves the dron from one place to another 
#the function returns the drone's current location while moving
#====================================================================================================
def takeOneStep(current_coords, goal_coords):
    print("*step*")
    c_long = current_coords[0]
    c_la = current_coords[1]
    g_long = goal_coords[0]
    g_la = goal_coords[1]
    k = ((g_la-c_la)/(g_long-c_long))
    d_long = ((0.00001**2)/(1+(k**2)))**(0.5)
    d_la = d_long*k
    if g_long < c_long:
        d_long = -d_long
    if g_la > c_la:
        d_la = -d_la
    print(k)
    print(d_long)
    print(d_la)
    print(c_long)
    print(c_la)
    print(g_long)
    print(g_la)
    #time.sleep(1/1000)
    return (c_long+d_long, c_la+d_la)
#====================================================================================================


def run(current_coords, from_coords, to_coords, SERVER_URL):
    # Compmelete the while loop:
    # 1. Change the loop condition so that it stops sending location to the data base when the drone arrives the to_address
    # 2. Plan a path with your own function, so that the drone moves from [current_address] to [from_address], and the from [from_address] to [to_address]. 
    # 3. While moving, the drone keeps sending it's location to the database.
    #====================================================================================================
    drone_coords = takeOneStep(current_coords, from_coords)
    limit = 0.00005
    # Go to start
    print("tag 1")
    print((round(abs(drone_coords[0] - from_coords[0]), 5) <= limit) and (round(abs(drone_coords[1] - from_coords[1]), 5) <= limit))
    while not ((round(abs(drone_coords[0] - from_coords[0]), 5) <= limit) and (round(abs(drone_coords[1] - from_coords[1]), 5) <= limit)):
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                              'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
        #print(drone_coords)
        #print(from_coords)
        #print(to_coords)
        drone_coords = takeOneStep(drone_coords, from_coords)

    # Go to finish
    print("tag 2")
    while not ((round(abs(drone_coords[0] - to_coords[0]), 5) <= limit) and (round(abs(drone_coords[1] - to_coords[1]), 5) <= limit)):
        with requests.Session() as session:
            drone_location = {'longitude': drone_coords[0],
                              'latitude': drone_coords[1]
                        }
            resp = session.post(SERVER_URL, json=drone_location)
        print(drone_coords)
        print(from_coords)
        print(to_coords)
        drone_coords = takeOneStep(drone_coords, to_coords)
    print("tag 3")
  #====================================================================================================

   
if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (round(args.flong, 5), round(args.flat, 5))
    to_coords = (round(args.tlong, 5), round(args.tlat, 5))

    print(current_coords)
    print(from_coords)
    print(to_coords)

    run(current_coords, from_coords, to_coords, SERVER_URL)

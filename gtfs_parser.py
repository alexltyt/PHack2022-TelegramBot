from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import datetime
import urllib.request
from transit_stop import getStopNamefromStopID
import termtables as tt

feed = gtfs_realtime_pb2.FeedMessage()

# Download latest trip pb
urllib.request.urlretrieve(
    "https://data.calgary.ca/download/gs4m-mdc2/application%2Foctet-stream",
    "tripupdates.pb",
)

# Deserialize the data to dict
with open("tripupdates.pb", "rb") as f:
    buff = f.read()

feed.ParseFromString(buff)
dict_obj = MessageToDict(feed)
vehicle_data = dict_obj["entity"]


# def getRouteBusStop(route_id: int):
#     bus_list = []
#     stop_list = []
#     for vehicle in vehicle_data:
#         if vehicle["tripUpdate"]["trip"]["routeId"] == str(route_id):
#             bus_list.append(vehicle)
#     for bus in bus_list:
#         bus_trips = bus["tripUpdate"]["stopTimeUpdate"]
#         # print(bus_trips[0])
#         if bus_trips[0]["stopSequence"] == 1:
#             for index, stop in enumerate(bus["tripUpdate"]["stopTimeUpdate"]):
#                 stop_list.append(
#                     f"{index+1}: {getStopNamefromStopID(stop['stopId'])}\n"
#                 )
#             return stop_list


def getBusSchedule(route_id: int):
    for vehicle in vehicle_data:
        if vehicle["tripUpdate"]["trip"]["routeId"] == route_id:

            stopTime = vehicle["tripUpdate"]["stopTimeUpdate"]
            schedule = [
                f"*------------- Route {route_id} || TripID {vehicle['id']} -------------*\n",
                "{0:75}{1:15}\n".format(
                    # "Stop",
                    "*Stop*",
                    "*Arrival Time*",
                    # "Departure Time",
                    # "Status",
                ),
            ]
            for stop in stopTime:
                if stop["scheduleRelationship"] == "SCHEDULED":
                    arrival_time = datetime.datetime.fromtimestamp(
                        int(stop["arrival"]["time"])
                    )
                    departure_time = datetime.datetime.fromtimestamp(
                        int(stop["departure"]["time"])
                    )
                    stopName = getStopNamefromStopID(stop["stopId"])
                    schedule.append(
                        "{0:75}{1:15}\n".format(
                            # str(stop["stopSequence"]),
                            stopName.strip(),
                            arrival_time.strftime("%H:%M"),
                            # departure_time.strftime("%H:%M"),
                            # stop["scheduleRelationship"],
                        )
                    )
            return schedule


if __name__ == "__main__":
    route = input("Which route:")
    print("".join(getBusSchedule(route)))

from google.transit import gtfs_realtime_pb2

feed = gtfs_realtime_pb2.FeedMessage()

with open("vehiclepositions.pb", "rb") as f:
    buff = f.read()

feed.ParseFromString(buff)

content = ""
counter = 0
for entity in feed.entity:
    if entity.HasField("vehicle"):
        counter += 1
        # content += '\n\n###############\nVehicle %d\n'%counter
        # content += entity.vehicle
print(counter)

print("Feed:")
print(feed)
print("#" * 40)

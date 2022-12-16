import json
import requests


def getStopNamefromStopID(stop_id: int):
    with open("stop_list.json", "r") as read_file:
        data = json.load(read_file)

    for stop in data:
        if stop["teleride_number"] == str(stop_id):
            return stop["stop_name"]


if __name__ == "__main__":
    print(getStopNamefromStopID(6348))

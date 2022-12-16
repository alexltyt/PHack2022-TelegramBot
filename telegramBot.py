from flask import Flask
from flask import request
from flask import Response
import requests

# import json
from gtfs_parser import getBusSchedule, getRouteBusStop

TOKEN = "5931334073:AAGPGxpuOyBraGzSbkSJm3VyawU7x3E6erQ"
app = Flask(__name__)


def parse_message(message):
    # print("message-->", message)
    chat_id = message["message"]["chat"]["id"]
    txt = message["message"]["text"]
    # print("chat_id-->", chat_id)
    # print("txt-->", txt)
    return chat_id, txt


def tel_send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}

    r = requests.post(url, json=payload)
    return r


# def tel_send_poll(chat_id, stopList):
#     url = f"https://api.telegram.org/bot{TOKEN}/sendPoll"
#     payload = {
#         "chat_id": chat_id,
#         "question": "In which direction does the sun rise?",
#         "options": json.dumps(stopList),
#         "is_anonymous": False,
#         "type": "quiz",
#         "correct_option_id": 2,
#     }
#     print(payload)
#     r = requests.post(url, json=payload)

#     return r


def tel_send_stopbutton(chat_id, stopList):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    option = []
    for index, stop in enumerate(stopList):
        option.append({"text": index, "callback_data": index})
    payload = {
        "chat_id": chat_id,
        "text": "What is this?",
        "reply_markup": {"keyboard": [option]},
    }
    r = requests.post(url, json=payload)
    return r


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        msg = request.get_json()

        chat_id, txt = parse_message(msg)
        if txt.lower() == "hi":
            tel_send_message(
                chat_id,
                "Hello!! This is a bot to save the late student, always check this before you leave home.\n'Please enter a bus route. (e.g. 65)",
            )
        elif isinstance(int(txt), int):
            route_id = int(txt)
            tel_send_message(chat_id, "".join(getBusSchedule(txt)))
            # tel_send_poll(chat_id, getRouteBusStop(txt))
        else:
            tel_send_message(chat_id, "Please enter a bus route. (e.g. 65)")

        return Response("ok", status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == "__main__":
    app.run(debug=True)

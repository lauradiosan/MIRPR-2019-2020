import webbrowser

import requests
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

from keras.models import load_model

model = load_model("chatbot_model.h5")
import spacy
from dateutil import parser

NLP = spacy.load("en_core_web_sm")

required_fields = {"location": "", "check-in": "", "duration": "", "adults": "", "rooms": ""}

response_missing_info = {
    "location": "Please tell me where you want to go.",
    "check-in": "When will you start your holiday?",
    "duration": "How many days will you stay?",
    "adults": "How many people are you?",
    "rooms": "How many rooms do you wish to book?",
}

# Creating GUI with tkinter
from tkinter import *


def get_location_id(location):
    url = "https://tripadvisor1.p.rapidapi.com/locations/search"

    querystring = {
        "location_id": "1",
        "limit": "30",
        "sort": "relevance",
        "offset": "0",
        "lang": "en_US",
        "currency": "USD",
        "units": "km",
        "query": location,
    }

    headers = {
        "x-rapidapi-host": "tripadvisor1.p.rapidapi.com",
        "x-rapidapi-key": "25713e1e5dmshe0ac4c928aee9a5p1e318djsn27ad4d4c8fc1",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()["data"][0]["result_object"]["location_id"]


def get_offer(location_id):
    url = "https://tripadvisor1.p.rapidapi.com/hotels/list"

    querystring = {
        "zff": "4%2C6",
        "offset": "0",
        "subcategory": "hotel",
        "hotel_class": "1%2C2%2C3",
        "currency": "USD",
        "child_rm_ages": "7%2C10",
        "limit": "30",
        "checkin": required_fields["check-in"],
        "order": "asc",
        "lang": "en_US",
        "sort": "recommended",
        "nights": required_fields["duration"],
        "location_id": location_id,
        "adults": required_fields["adults"],
        "rooms": required_fields["rooms"],
    }

    headers = {
        "x-rapidapi-host": "tripadvisor1.p.rapidapi.com",
        "x-rapidapi-key": "25713e1e5dmshe0ac4c928aee9a5p1e318djsn27ad4d4c8fc1",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    offers = response.json()["data"][0]["hac_offers"]["offers"]

    for offer in offers:
        if offer["is_bookable"]:
            return offer["link"]


def analyze_input(msg):
    doc = NLP(msg)

    for ent in doc.ents:
        text = ent.text
        label = ent.label_

        print(text, label)

        if label == "GPE" or label == "PERSON" or label == "LOC":
            required_fields["location"] = text
        elif label == "DATE":
            try:
                text = text.replace("the", "")
                date = parser.parse(text)
                required_fields["check-in"] = str(date).split(" ")[0]
            except:
                text = text.replace("days", "")
                text = text.replace("day", "")
                text = text.replace("nights", "")
                text = text.replace("night", "")
                required_fields["duration"] = text.strip()
        elif label == "CARDINAL":
            left = len(required_fields) - sum([1 for r in required_fields.values() if r])
            if left == 1:
                required_fields["rooms"] = text
            else:
                required_fields["adults"] = text

    for key, value in required_fields.items():
        if not value:
            return response_missing_info[key]

    location_id = get_location_id(required_fields["location"])

    offer = get_offer(location_id)

    print(offer)
    ChatLog.bind("<Button-1>", lambda e: webbrowser.open(offer))

    return "Click me to navigate to the webpage with your offer"


def send():
    msg = EntryBox.get("1.0", "end-1c").strip()
    EntryBox.delete("0.0", END)

    if msg != "":
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + "\n\n")
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        response = analyze_input(msg)

        ChatLog.insert(END, "Bot: " + str(response) + "\n\n")
        print(required_fields)

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Chatbot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial", cursor="hand2")

ChatLog.config(state=DISABLED)

# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog["yscrollcommand"] = scrollbar.set

# Create Button to send message
SendButton = Button(
    base,
    font=("Verdana", 12, "bold"),
    text="Send",
    width="12",
    height=5,
    bd=0,
    bg="#32de97",
    activebackground="#3c9d9b",
    fg="#ffffff",
    command=send,
    cursor="hand2",
)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")
# EntryBox.bind("<Return>", send)


# Place all components on the screen
scrollbar.place(x=376, y=6, height=386)
ChatLog.place(x=6, y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

ChatLog.config(state=NORMAL)
ChatLog.insert(
    END,
    "Bot: Hi there! I'm here to help so tell me more about where you want to spend you holiday"
    + "\n\n",
)
ChatLog.config(foreground="#442265", font=("Verdana", 12))

base.mainloop()

from django.shortcuts import render, redirect
from django import template
from django.core.files import File

from chat.responses import RESPONSES
from services.holiday_chatbot_service import HolidayChatbotService

import os
import io
import zipfile

REGISTER = template.Library()

INITIAL_RESPONSES_LIST = [{'template': 'received_chat_box.html',
                           'text_to_display': RESPONSES['initialResponse']}]


def index(request):
    responses_list = request.session.get("responses_list", INITIAL_RESPONSES_LIST)
    request.session["responses_list"] = responses_list
    context = {
        "responses_list": responses_list
    }
    return render(request, 'index.html', context)


def reset(request):
    holiday_chatbot_service = HolidayChatbotService()
    holiday_chatbot_service.reset()
    if request.session.get('responses_list', None):
        del request.session['responses_list']
    return redirect("../")


def send_text(request):
    if request.method == 'POST' and 'reset' in request.POST:
        return reset(request)

    image = request.FILES.get('image', '')
    if image:
        return analyse_image(request, image)

    input_text = request.POST.get('input-text', '')
    if input_text:
        return analyse_text(request, input_text)
       
    return redirect("../")

def analyse_image(request, image):
    responses_list = request.session.get("responses_list", [])
    responses_list.append({'template': 'sent_chat_box.html',
                        'text_to_display': 'Image uploaded.'})
    request.session["responses_list"] = responses_list
    holiday_chatbot_service = HolidayChatbotService()
    vacation_requirements = holiday_chatbot_service.analyse_image(image)
    return set_repsonse(request, vacation_requirements, responses_list)


def analyse_text(request, input_text):
    responses_list = request.session.get("responses_list", [])
    responses_list.append({'template': 'sent_chat_box.html',
                        'text_to_display': input_text})

    holiday_chatbot_service = HolidayChatbotService()
    vacation_requirements = holiday_chatbot_service.analyze_text(input_text)
    return set_repsonse(request, vacation_requirements, responses_list)


def set_repsonse(request, vacation_requirements, responses_list):
    if vacation_requirements is None:
        responses_list.append({'template': 'received_chat_box.html',
                               'text_to_display': RESPONSES['backendFailure']})
        request.session["responses_list"] = responses_list
        return redirect("../")

    return add_next_response_and_redirect(request, vacation_requirements, responses_list)


def add_next_response_and_redirect(request, vacation_requirements, responses_list):
    if vacation_requirements.are_all_required_set():
        return redirect_final_response(request, vacation_requirements, responses_list)

    if not vacation_requirements.cities and not vacation_requirements.start_date \
       and not vacation_requirements.end_date:
        responses_list.append({'template': 'received_chat_box.html',
                               'text_to_display': RESPONSES['noLocationNoDates']})
        request.session["responses_list"] = responses_list
        return redirect("../")

    if not vacation_requirements.cities:
        responses_list.append({'template': 'received_chat_box.html',
                               'text_to_display': RESPONSES['noLocation']})
        request.session["responses_list"] = responses_list
        return redirect("../")

    if not vacation_requirements.start_date or not vacation_requirements.end_date:
        responses_list.append({'template': 'received_chat_box.html',
                               'text_to_display': RESPONSES['noDates']})
        request.session["responses_list"] = responses_list
        return redirect("../")

    if not vacation_requirements.number_of_rooms:
        responses_list.append({'template': 'received_chat_box.html',
                            'text_to_display': RESPONSES['noNumberOfRooms']})
        request.session["responses_list"] = responses_list
        return redirect("../")

    # number_of_children not set.
    responses_list.append({'template': 'received_chat_box.html',
                           'text_to_display': RESPONSES['noNumberOfChildren']})
    request.session["responses_list"] = responses_list
    return redirect("../")


# Text to get here:
# I want to go to London, between 01-20-2020 and 01-22-2020. I have 4 kids and we'll need two rooms.
def redirect_final_response(request, vacation_requirements, responses_list):
    holiday_chatbot_service = HolidayChatbotService()
    hotels_list = holiday_chatbot_service.get_hotels_list()
    if not hotels_list:
        responses_list.append({'template': 'received_chat_box.html',
                               'text_to_display': RESPONSES['noHotelsFound']})
        request.session["responses_list"] = responses_list
        return redirect("../")

    hotels_list = hotels_list[0:3]
    for hotel in hotels_list:
        # TODO: fix this. works for now
        hotel_id = hotel['hotel_id']
        hotel['positive_reviews_wordcloud'], hotel['negative_reviews_wordcloud'] = \
             extract_reviews_wordcloud(holiday_chatbot_service, hotel_id)

    responses_list.append({'template': 'final_response_chat_box.html',
                           'text_to_display': 'Here is the top accomodation '\
                                              'that matches your requests: ',
                           'accomodations_list': hotels_list})
    request.session["responses_list"] = responses_list
    return redirect("../")


def extract_reviews_wordcloud(holiday_chatbot_service, hotel_id):
    positive_reviews_image_name = \
        str(hotel_id) + '_positive_reviews_wordcloud.png'
    negative_reviews_image_name = \
        str(hotel_id) + '_negative_reviews_wordcloud.png'
    image_path = "/home/adriana/Documents/chatbot/project/client/client/media/"
    positive_reviews_image_path = image_path + positive_reviews_image_name
    negative_reviews_image_path = image_path + negative_reviews_image_name

    # No need to make a call to retrieve them if they're already on the client.
    if os.path.exists(positive_reviews_image_path) and os.path.exists(negative_reviews_image_path):
        return '/media/' + positive_reviews_image_name, '/media/' + negative_reviews_image_name

    reviews_image_zip = holiday_chatbot_service.get_hotel_reviews_wordcloud(hotel_id) 
    z = zipfile.ZipFile(io.BytesIO(reviews_image_zip), 'r',  compression=zipfile.ZIP_DEFLATED)
    z.extractall(path=image_path)
    z.close()
    
    return '/media/' + positive_reviews_image_name, '/media/' + negative_reviews_image_name

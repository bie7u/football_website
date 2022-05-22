from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import requests
# yomamabot/fb_yomamabot/views.py
from django.views import generic
from django.http.response import HttpResponse
from pymessenger2.bot import Bot
from pymessenger2 import Element
from user_panel.models import ActualMatchs
# Create your views here.
# yomamabot/fb_yomamabot/views.py

# 
def send__all__matches(user_id):
    bot = Bot('EAAKJqqfPCVoBAD66oNpda6TlmIvd14UlKeYexKHV9DY6R8RkzgaV3XubGHyWmDZB9MX8zlZAyEj263HddOnYxKOF8j5ZB0k1uAQCxyNEmtRVIs7n5IM23D91QkFRRzMIU8eUCBQLINRtE7otG0p4ubKr5f2bLZA2xi4stpvbqzZCvqoZA7cQU4')
    bot.send_text_message(user_id, 'Witam, aktualnie trwają następujące mecze, wybierz ten który Cię interesuje i zaktualizuj wynik.')
    for match in ActualMatchs.objects.filter(live=True):
        
        elements = []
        element = Element(title=f"{str(match.team_home)} - {str(match.team_versus)}", subtitle=f"{str(match.league)}", buttons=[{
                    "type":"web_url",
                    "url":f"https://first-bl-app.herokuapp.com/edit_live/{match.team_home.id}/{match.team_versus.id}/",
                    "title":"Zaktualizuj wynik"
        }])
        elements.append(element)

        bot.send_generic_message(user_id, elements)


class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '123456':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    user_id = list(list(message.values())[0].values())[0]
                    print(message)
                    send__all__matches(user_id)    
        return HttpResponse()



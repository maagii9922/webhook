from django.http import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re

import random

import requests

PAGE_ACCESS_TOKEN = "EAANZA3YNaNMEBAGANyI222q2bM4rTgHGZBHy4bggKyIJITs36XlI07mU0USiiVNM8M5GPB7Fj8DL83dneKWgHoe7S8Gy3VuEw3TQHaofY4z20gRkNUkYt1orW91gPUZCWcJMJZAiSKrqIS6EM3mcrngaaRJkfepRIKNlG8pqXMhb9l4EAkA5"
VERIFY_TOKEN = "2318934571"

class BotView(generic.View):

    def get(self, request, *args, **kwargs):
        # print(self.request.GET['asljflsdjflasdjfa'] )
        
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')



    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)



    def post(self, request, *args, **kwargs):
        # AA = json.loads(self.request.body.decode('utf-8'))
        # print(                AA["hub.verify_token"]   )

        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            # print(entry)
            for message in entry['messaging']:
                # print(message)
                if 'message' in message:
                    # print(message['message'])
        #             pprint(message)
                    post_facebook_message(
                        message['sender']['id'], message['message']['text'])
        return HttpResponse()

jokes = {
    u'холбоо барих': [u"""холбоо барих-1.""", u"""холбоо барих-2."""],
    u'түгээмэл асуулт хариулт': [u"""түгээмэл асуулт хариулт-1.""", u"""түгээмэл асуулт хариулт-2"""],
    u'эхлэх': [u"""эхлэх-1""", u"""эхлэх-2."""]
}

def post_facebook_message(fbid, recevied_message):
    # print(arg1, arg2)
    tokens = re.sub(r"[^a-zA-Z0-9А-я,\s]", '*', recevied_message).lower().split(',')
    print(tokens)
    joke_text = ''
    for token in tokens:
        if token in jokes:
            # print('olfloo')
            joke_text = random.choice(jokes[token])
            print(joke_text)
            break
    if not joke_text:
        print(u"Би ойлгосонгүй! Бидэн уруу 'Холбоо барих', 'Түгээмэл асуулт хариулт', 'Эхлэх' гэж илгээнэ үү!")
    

    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {
        'fields': 'first_name,last_name', 'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = 'Yo ' + user_details['first_name'] + '..! ' + joke_text


    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    response_msg = json.dumps(
        {"recipient": {"id": fbid}, "message": {"text": joke_text}})
    status = requests.post(post_message_url, headers={
                           "Content-Type": "application/json"}, data=response_msg)

    print(joke_text)
    return HttpResponse(joke_text)
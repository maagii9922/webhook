from django.http import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re

import random

PAGE_ACCESS_TOKEN = "DQVJ2ZATUxOVUtdllmbk9VT0g4T3Q0WmY0SXg1MnBRZAVdaN0MzeVpqNUh2RGZAHeDlvSDIwUkV6ZAWs3WEFOck5CSk83VTV0cHk2bmh3VS16X1BuY3RrUENqdG9QZAVprTnNzajRhY196WVZARM2FIMm5RZAVV3cjBSbGc5azVlaUJsNVJwck1QUG5fbG1DaTZAZAU2Vpdkd4bXJzMF9OeHhqS3Bpamtmb3A3aTc2dnJNTXNGS1JnRmFOMzJ6YUdMc2Vvd01UNGFwcHdzeV9SYlhWbWxZAQQZDZD"
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
    print(joke_text)
    return HttpResponse(joke_text)
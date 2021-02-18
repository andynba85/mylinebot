from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
#from linebot.models import MessageEvent, TextSendMessage
from linebot.models import *
from newsbot.models import *
import  requests
from  bs4  import  BeautifulSoup

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def  technews ():
    target_url  =  'https://technews.tw/category/ai/'
    print ( 'Start parsing movie ...' )
    rs  =  requests . session ()
    res  =  rs . get ( target_url , verify = False )
    res . encoding  =  'utf-8'
    soup  =  BeautifulSoup ( res . text , 'html.parser' )
    content  =  ""

    for  index , data  in  enumerate ( soup . select ( 'article div h1.entry-title a' )):
        if  index  ==  12 :
            return  content
        title  =  data . text
        link  =  data [ 'href' ]
        content  +=  '{} \n {} \n \n ' . format ( title , link )
    return  content


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

'''
    if request.method == 'POST':
        #先設定一個要回傳的message空集合
        message=[]
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        #在這裡將body寫入機器人回傳的訊息中，可以更容易看出你收到的webhook長怎樣#
        #message.append(TextSendMessage(text=str(body)))

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            #如果事件為訊息
            if isinstance(event, MessageEvent):
                print(event.message.type)
                if event.message.type=='text':
                    
                
                    if  event . message . text  ==  "科技新報" :
                        content  =  technews ()
                        print(content)
                        line_bot_api . reply_message (
                            event . reply_token ,
                            TextSendMessage ( text = content ))
                        return  0
                    
                    
                    #爬取科技新報ai專欄的資料
                    if  event.message.text  ==  "科技新報" :
                        content = technews ()
                        message.append(TextSendMessage(text=content))
                        line_bot_api.reply_message(event.reply_token,message)
                    elif(event.message.text  ==  "記帳"):
                        buttons_template = TemplateSendMessage(
                            alt_text='開始記帳',
                            template=ButtonsTemplate(
                                title='選擇服務',
                                text='請選擇',
                                thumbnail_image_url='https://i.imgur.com/pm1vdnI.jpg',
                                actions=[
                                    MessageTemplateAction(
                                        label='新增',
                                        text='新增'
                                    ),
                                    MessageTemplateAction(
                                        label='查詢',
                                        text='查詢'
                                    ),
                                    MessageTemplateAction(
                                        label='刪除',
                                        text='刪除'
                                    ),
                                    MessageTemplateAction(
                                        label='月',
                                        text='月'
                                    )
                                ]
                            )
                        )
                        line_bot_api.reply_message(event.reply_token, buttons_template)
                    else:
                        message.append(TextSendMessage(text='文字訊息'))
                        line_bot_api.reply_message(event.reply_token,message)
                    #message.append(TextSendMessage(text='文字訊息'))
                    

                elif event.message.type=='image':
                    message.append(TextSendMessage(text='圖片訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='location':
                    message.append(TextSendMessage(text='位置訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='video':
                    message.append(TextSendMessage(text='影片訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='sticker':
                    message.append(TextSendMessage(text='貼圖訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='audio':
                    message.append(TextSendMessage(text='聲音訊息'))
                    line_bot_api.reply_message(event.reply_token,message)

                elif event.message.type=='file':
                    message.append(TextSendMessage(text='檔案訊息'))
                    line_bot_api.reply_message(event.reply_token,message)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
'''
# -*- coding: utf8 -*-
import json
import requests
import os
os.environ["PYTHONIOENCODING"]="UTF8"

# запись лога в файл
def write(content):
    f = open('text.txt', 'a')
    f.write(content)
    f.close()

# https://yandex.ru/dev/dialogs/alice/doc/protocol.html/
def genResp(data):
# content='{"response": {"text": "'+command+'","tts": "<speaker effect=\'train_announce\'>'+command+'","end_session": false}, "version": "1.0"}'
# content='{"response": {"text": "'+command+'","tts": "<speaker audio=\'alice-music-drum-loop-1.opus\'>'+tmp+'","end_session": false}, "version": "1.0"}'
    return '{"response": {"text": "'+data['text']+'","tts": "'+data['tts']+'","end_session": false}, "version": "1.0"}'

# запрос датчиков из проекта http://narodmon.ru/api
def getSensor(sensorId):
    uuid="dfd9f272d50b18c57d4114ce2f75a25c" # md5
    api_key="70AHehB2MqnTx"
    req={"cmd":"sensorsValues","sensors":[sensorId],"uuid":uuid,"api_key":api_key}
    dat=json.dumps(req)
    response=requests.post('http://narodmon.ru/api',data=dat)
    res=response.content
    if res!='':
        r=json.loads(res)
        return r['sensors'][0]['value']
    else:
        return res

# основная функция генерации ответов Алисы
# на вход подается json данные сгенерированные Алисой
def answer(request):
    content="""{
 "response": {
    "text": "Empty",
    "tts": "Eeempty",
    "end_session": false
  },
  "version": "1.0"
}"""
    if request!='':
        j = json.loads(request)
        command = j['request']['command']
        if command == 'бит':
            data={"text":"суупер биит","tts":'с+упер б+ит'}
            content=genResp(data)
        # запрос температуры
        elif command in ['температура на улице','температура за окном','алиса температура на улице','алиса температура за окном']:
            temp=getSensor(7466)
            if temp!='':
                say="температура за окном: "+str(temp)+' градусов'
                say=say
                data={"text":say,"tts":say}
            else:
                data={"text":"а я не знаю","tts":'а я не знаю'}
            content=genResp(data)
        # запрос давления
        elif command in ['давление на улице','давление за окном','алиса давление на улице','алиса давление за окном']:
            pressure=getSensor(955)
            if pressure!='':
                say="атмосферное давление: "+str(pressure)+' миллиметров ртутного столба'
                say=say
                data={"text":say,"tts":say}
            else:
                data={"text":"а я не знаю","tts":'а я не знаю'}
            content=genResp(data)
        else:
            data={"text":command,"tts":command}
            content=genResp(data)
    write(content)
    return content


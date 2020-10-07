# -*- coding: utf8 -*-
import json
import requests

# запись лога в файл
def write(content):
    f = open('text.txt', 'a')
    f.write(content + '\n')
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
        if command == 'бит'.decode('utf8'):
            data={"text":"суупер биит".decode('utf8'),"tts":'с+упер б+ит'.decode('utf8')}
            content=genResp(data)
        # запрос температуры
        if command == 'температура на улице'.decode('utf8'):
            temp=getSensor(7466)
            if temp!='':
                say="температура за окном: "+str(temp)+' градусов'
                say=say.decode('utf8')
                data={"text":say,"tts":say}
            else:
                data={"text":"а я не знаю".decode('utf8'),"tts":'а я не знаю'.decode('utf8')}
            content=genResp(data)
        # запрос давления
        if command == 'давление на улице'.decode('utf8'):
            pressure=getSensor(955)
            if pressure!='':
                say="атмосферное давлен: "+str(pressure)+' миллиметров ртутного столба'
                say=say.decode('utf8')
                data={"text":say,"tts":say}
            else:
                data={"text":"а я не знаю".decode('utf8'),"tts":'а я не знаю'.decode('utf8')}
            content=genResp(data)
        else:
            data={"text":command,"tts":command}
            content=genResp(data)
    write(content.encode('utf8'))
    return content

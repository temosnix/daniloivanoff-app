import json
import pandas as pd
import requests
from datetime import datetime
from helpers import tratar_informacao


autorizacao = "Bearer APP_USR-2417001236894079-081607-b066d31ea3c036713fa51f764385623b-34977269"

def Perguntas(id_pergunta):
    data = '''{
                "_id": "2d0edf52-1e8e-4e51-a9d1-48ee6d6735d5",
                "topic": "questions",
                "resource": "/questions/12808956513",
                "user_id": 34977269,
                "application_id": 2417001236894079,
                "sent": "2023-08-16T13:01:38.48Z",
                "attempts": 1,
                "received": "2023-08-16T13:01:38.443Z"
            }'''
    data_dict = json.loads(data)
    tratar_informacao(data)

def mensagens():

    url = f"https://api.mercadolibre.com/messages/{id_mensagem}"

    payload = {}
    headers = {
    'Authorization': autorizacao
    }

    response = requests.request("GET", url, headers=headers, arquivo=payload)

    print(response.text)

def vendas(id_nova_compra):
    

    url = f"https://api.mercadolibre.com/orders/{id_nova_compra}"

    payload = {}
    headers = {
    'Authorization': autorizacao
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    arquivo = response.json()

   
    print(arquivo['tags'])
    id_compra = arquivo["id"]
    primeiro_item = arquivo["order_items"][0]["item"]
    item_id = primeiro_item["id"]
    item_title = primeiro_item["title"]
    quantidade = arquivo["order_items"][0]["quantity"]

    comprador = arquivo['buyer']
    date_created = arquivo['date_created']
    nickname = comprador['nickname']
    nome = comprador['first_name'] + " " + comprador['last_name']
  


   
    data_hora_atual = datetime.now()
    dia_atual = data_hora_atual.day
    mes_atual = data_hora_atual.month
    ano_atual = data_hora_atual.year

    data_obj = datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%S.%f%z")
    data_compra = data_obj.strftime("%d-%m-%y")
    dia_compra = data_obj.day
    mes_compra = data_obj.month
    ano_compra = data_obj.year

    print(f'\n id da compra : {id_compra} \n\n data da compra: {data_compra}\n\n id do anuncio: {item_id} \n\n titulo do anuncio: {item_title}\n\n nome do cliente :{nome}\n\n quantidade: {quantidade}\n' )


id_perg = "12809084003"
id_mensagem = "89060a3c058346b58f097f4cb4e88dcf"
id_nova = "2000006273382296"

#vendas(id_nova)

mensagens(id_mensagem)
#Perguntas(id_perg)
def teste():
      data = '''{
                "_id": "2d0edf52-1e8e-4e51-a9d1-48ee6d6735d5",
                "topic": "questions",
                "resource": "/questions/12808956513",
                "user_id": 34977269,
                "application_id": 2417001236894079,
                "sent": "2023-08-16T13:01:38.48Z",
                "attempts": 1,
                "received": "2023-08-16T13:01:38.443Z"
            }'''
      data_dict = json.loads(data)
      print(data_dict['topic'])

#teste()
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from django.http import HttpResponse
from testeapp.models import Reflesh_Tokens, Access_token



def Renovar():
    
    tabela_refresh = Reflesh_Tokens.objects.get(id=1)
    
    rf_tokens = tabela_refresh.Rf_tokens
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    url = "https://api.mercadolibre.com/oauth/token"

    payload = f'grant_type=refresh_token&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&refresh_token={rf_tokens}'
    headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json()['access_token'])
    print(response.json()['refresh_token'])

    if response.status_code == 200:

        dados = response.json()
        rf_novo = (dados["refresh_token"])
        ac_novo = (dados["access_token"])

        data_atual = datetime.now()
        data_str = data_atual.strftime("%Y-%m-%d")
        
        tabela_refresh.Data_refresh = datetime.strptime(data_str, "%Y-%m-%d").date()
    
        tabela_refresh.Hora_refresh = datetime.now().time()
        tabela_refresh.Rf_tokens = rf_novo
        tabela_refresh.save()


        rt = Reflesh_Tokens.objects.get(id=1)   
        data_refresh = str(rt.Data_refresh)
        


        tabela_access = Access_token.objects.get(id=1)
        tabela_access.AC_token = ac_novo
        tabela_access.save()

        
    else:
        print(f'A autenticação do Token falhou. Cod : {response.text}')
    return ('ok')
    
def Tempo ():


   
    rt = Reflesh_Tokens.objects.get(id=1)   
    data_refresh = str(rt.Data_refresh)
    data_atual = datetime.now()
    data_str = data_atual.strftime("%Y-%m-%d")
 
    hora_bd = rt.Hora_refresh
    hora_formatada = datetime.now().time()
    
    if data_refresh == data_str:
        
        segundos = (((data_atual.hour*3600) + (data_atual.minute*60) + data_atual.second) - ((rt.Hora_refresh.hour*3600) + (rt.Hora_refresh.minute*60) + rt.Hora_refresh.second)) 
        if segundos > 21600:
            
            resposta = Renovar()
            
            
    else:
        
        segundos = (86400 - ((rt.Hora_refresh.hour*3600) + (rt.Hora_refresh.minute*60) + rt.Hora_refresh.second)) + ((data_atual.hour*3600) + (data_atual.minute*60) + data_atual.second)
        if segundos > 21600:
       
            resposta = Renovar()
            

    return HttpResponse(segundos)






def dados_cliente_compra(id_venda,access_token):

    url = f"https://api.mercadolibre.com/orders/{id_venda}"

    payload = {}
    headers = {
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    #print(response.text)
    resultado = {}
    resultado['quantidade'] = response.json()["order_items"][0]["quantity"]
    resultado['nome']= response.json()['buyer']['first_name'] + " " + response.json()['buyer']['last_name']
    resultado['titulo'] = item_title = response.json()["order_items"][0]["item"]["title"]
    data_compra = datetime.strptime(response.json()['date_created'], '%Y-%m-%dT%H:%M:%S.%f%z')
    resultado['data_compra'] = data_compra.strftime('%d/%m/%y')
    resultado['id_anuncio'] = response.json()["order_items"][0]["item"]['id']

    return (resultado)

def pack(id,access_token,nome):

    url = f"https://api.mercadolibre.com/messages/packs/{id}/sellers/34977269?tag=post_sale"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    total_msg = response.json()['paging']['total']
    print(type(total_msg))
    print(total_msg)
    if total_msg > 10 :
        total_msg = 10
    

    for i in range(total_msg - 1, -1, -1):
        
        usuario = (response.json()['messages'][i]['from']['user_id'])
        if usuario == 34977269:

            print(f"  Dfast :{response.json()['messages'][i]['text']}")
        else:
            print(f"{nome} :{response.json()['messages'][i]['text']}")


def tratar_info(data):
    ''' exemplo do data.json recebido. topic pode alterar entre : orders_v2, messages e questions
        {
        "_id": "2827bcb2-ab15-4776-8e87-084eb8e421f8",
        "topic": "orders_v2",
        "resource": "/orders/2000006313601192",
        "user_id": 34977269,
        "application_id": 2417001236894079,
        "sent": "2023-08-25T13:52:58.409Z",
        "attempts": 2,
        "received": "2023-08-25T13:51:54.759Z"
        }'''

    Tempo()
    tabela_refresh = Access_token.objects.get(id=1)
    access_token = tabela_refresh.AC_token
    

    topico = data['topic']
    
    if topico == 'orders_v2':


        resource = data['resource'].split("/")[-1]

        resposta = dados_cliente_compra(resource,access_token)
        
        data_atual = datetime.now()
        data_formatada = data_atual.strftime('%d/%m/%y')

        if resposta['data_compra'] == data_formatada:
            print('_________NOVA COMPRA ___________')
            for chave, valor in resposta.items():
                print(f'{chave}: {valor}')


    elif topico == 'messages':
        print('____________Nova Mensagem______________')

        resource = data["resource"]
            
        url =f"https://api.mercadolibre.com/messages/{resource}?tag=post_sale"

        payload = {}
        headers = {
        'Authorization': f'Bearer {access_token}'
        }

        response_msg = requests.request("GET", url, headers=headers, data=payload)

        id_pack = response_msg.json()['messages'][0]['message_resources'][0]['id']

        resposta = dados_cliente_compra(id_pack,access_token)
        nome = resposta['nome']

        pack(id_pack,access_token,nome)

    else:
        print(' ____________New Question____________')
        resource = data["resource"].split("/")[-1]
        print(resource)


        url = f"https://api.mercadolibre.com/questions/{resource}"

        payload = {}
        headers = {
        'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:

            if response.json()['status'] == 'ANSWERED':

                print(f' Pergunta:{response.json()["text"]}')
                print(f'   Resposta: {response.json()["answer"]["text"]}')
            else:

                print(f' Pergunta:{response.json()["text"]}')
                print(f'   Resposta:')
        else:

            print(f'erro ao procurar a pergunta. Erro : {response.status_code}')
  
    return 'ok'
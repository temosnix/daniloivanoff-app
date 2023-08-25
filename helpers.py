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
    print(response.text)
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

def tratar_info(j_dict):
    
    
    attempts = j_dict['attempts']
    topico = j_dict['topic']
    print(f'entrei no attempts = 1, tentando acessar o topico {topico}')
   
    
    Tempo()
    
    tabela_refresh = Access_token.objects.get(id=1)

    access_token = tabela_refresh.AC_token

    if topico == 'orders_v2':


        id_venda = j_dict['resource'].split("/")[-1]
        (id_venda)
    
        url = f"https://api.mercadolibre.com/orders/{id_venda}"

        payload = {}
        headers = {
        'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        
        response_orders = response.json()           
        data_obj = datetime.strptime(response_orders['date_created'], "%Y-%m-%dT%H:%M:%S.%f%z")
        dia_compra = data_obj.day            
        dia_atual = datetime.now().day


        if response.status_code == 200 and dia_atual == dia_compra :

            print(  '--- NOVA COMPRA --- ')


            id_compra = response_orders["id"]                
            nome = response_orders['buyer']['first_name'] + " " + response_orders['buyer']['last_name']
            item_title = response_orders["order_items"][0]["item"]["title"]
            quantidade = response_orders["order_items"][0]["quantity"]
            data_compra = data_obj.strftime("%d-%m-%y")
            id_anuncio = response_orders["order_items"][0]["item"]["id"]
            
            
            print(f'\n id da compra : {id_compra} \n\n data da compra: {data_compra}\n\n id do anuncio: {id_compra} \n\n titulo do anuncio: {item_title}\n\n nome do cliente :{nome}\n\n quantidade: {quantidade}\n' )

            if id_anuncio == 'MLB2015443547':
                
                url = f"https://api.mercadolibre.com/messages/packs/{id_compra}/sellers/34977269?tag=post_sale"

                payload = {}
                headers = {
                        'Authorization': f'Bearer {access_token}'
                }

                response = requests.request("GET", url, headers=headers, data=payload)


                print(f'saiu um civic 2012.. tentando enviar mensagem. Cod : {response.status_code}')


                if response.status_code == 200:
                    print(' cod: 200, verificando se existe conversa ativa')
                    status = response.json()["conversation_status"]['status']
                    if status == 'active':
                        print('jã existe uma conversa, verifique se já foi perguntado!')
                    else:
                        if status == 'blocked':

                            url = f"https://api.mercadolibre.com/messages/action_guide/packs/{id_compra}/option"

                            headers = {
                                "Authorization": f'Bearer {access_token}',
                                "Content-Type": "application/json"
                            }

                            data = {
                                "option_id": "OTHER",
                                "text": f"Olá {nome}, existe 2 tipos de amortecedor para seu carro. Me confirma se seu carro é 1.8 ou 2.0?"
                            }

                        response = requests.post(url, headers=headers, json=data)
                else:
                    print(response.text)
    else:


        if topico == 'questions':
            print('entrando em questions')
            
            resource = j_dict["resource"].split("/")[-1]
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

        else:

            if topico == 'messages':

                def pack(id):


                    url = f"https://api.mercadolibre.com/messages/packs/{id}/sellers/34977269?tag=post_sale"

                    payload = {}
                    headers = {
                        'Authorization': 'Bearer APP_USR-2417001236894079-082507-a8c030e7678e770e9de340f612cc1ecc-34977269'
                    }

                    response = requests.request("GET", url, headers=headers, data=payload)

                    total_msg = int(response.json()['paging']['total'])
                    
                    if total_msg > 10 :
                        total_msg = 10
                    

                    for i in range(total_msg - 1, -1, -1):
                        
                        usuario = (response.json()['messages'][i]['from']['user_id'])
                        if usuario == 34977269:

                            print(f"  Dfast :{response.json()['messages'][i]['text']}")
                        else:
                            print(f"Comprador :{response.json()['messages'][i]['text']}")

                    

                
                resource = j_dict["resource"]
                    
                url =f"https://api.mercadolibre.com/messages/{resource}?tag=post_sale"

                payload = {}
                headers = {
                'Authorization': 'Bearer APP_USR-2417001236894079-082507-a8c030e7678e770e9de340f612cc1ecc-34977269'
                }

                response = requests.request("GET", url, headers=headers, data=payload)

                pack(response.json()['messages'][0]['message_resources'][0]['id'])
            else:
                print(f'topico nao encontrado {topico} ')
  
    return 'ok'
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
    #print(response.text)
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

   
    if attempts == 1 :
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

           
            j_dict = response.json()
            id_compra = j_dict["id"]
            primeiro_item = j_dict["order_items"][0]["item"]
            item_id = primeiro_item["id"]
            item_title = primeiro_item["title"]
            quantidade = j_dict["order_items"][0]["quantity"]
            comprador = j_dict['buyer']
            nickname = comprador['nickname']
            nome = comprador['first_name'] + " " + comprador['last_name']

            date_created = j_dict['date_created']
            data_obj = datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%S.%f%z")
            data_compra = data_obj.strftime("%d-%m-%y")
            dia_compra = data_obj.day
            data_hora_atual = datetime.now()
            dia_atual = data_hora_atual.day

            print(f'\n id da compra : {id_compra} \n\n data da compra: {data_compra}\n\n id do anuncio: {item_id} \n\n titulo do anuncio: {item_title}\n\n nome do cliente :{nome}\n\n quantidade: {quantidade}\n' )

            if response.status_code == 200 and dia_atual == dia_compra :
                print(  '--- NOVA COMPRA --- ')

                arquivo = response.json()
                primeiro_item = arquivo["order_items"][0]["item"]
                id_anuncio = primeiro_item["id"]

                if id_anuncio == 'MLB2015443547':
                    id_compra = arquivo["id"]
                    comprador = arquivo['buyer']
                    date_created = arquivo['date_created']
                    nickname = comprador['nickname']
                    nome = comprador['first_name'] + " " + comprador['last_name']

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
                j_dict = json.loads(data)
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
                    print('entrando em messages')
                    resource = j_dict["resource"]
                    print(resource)
                    url =f"https://api.mercadolibre.com/messages/{resource}?tag=post_sale"

                    payload = {}
                    headers = {
                    'Authorization': f'Bearer {access_token}'
                    }

                    response = requests.request("GET", url, headers=headers, data=payload)

                    print(response.text)
                else:
                    print(f'topico nao encontrado {topico} ')
    else:
        print('attempts = 2 ou nao encontrado')
    return 'ok'
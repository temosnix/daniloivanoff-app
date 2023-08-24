import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from django.http import HttpResponse
from testeapp.models import Reflesh_Tokens, Access_token



def Renovar():
    print("entrei em renovar")
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
        print('code 200')
        rf_novo = (dados["refresh_token"])
        ac_novo = (dados["access_token"])

        data_atual = datetime.now()
        data_str = data_atual.strftime("%Y-%m-%d")
        
        tabela_refresh.Data_refresh = datetime.strptime(data_str, "%Y-%m-%d").date()
        tabela_refresh.Hora_refresh = datetime.now().time()
        tabela_refresh.Rf_tokens = rf_novo
        tabela_refresh.save()

        tabela_access = Access_token.objects.get(id=1)
        tabela_access.AC_token = ac_novo
        tabela_access.save()

        
    else:
        print(response.text)
    return ('ok')
    
def Tempo ():


    print('iniciando tempo')
    rt = Reflesh_Tokens.objects.get(id=1)   
    data_refresh = str(rt.Data_refresh)
    data_atual = datetime.now()
    data_str = data_atual.strftime("%Y-%m-%d")
 
    hora_bd = rt.Hora_refresh
    hora_formatada = datetime.now().time()
    print(f'data do banco de dados {data_refresh} data atual {data_str}')
    print(f'Hora do banco de dados {hora_bd} hora atual {hora_formatada}')
    if data_refresh == data_str:
        print(data_refresh,data_str)
        segundos = (((data_atual.hour*3600) + (data_atual.minute*60) + data_atual.second) - ((rt.Hora_refresh.hour*3600) + (rt.Hora_refresh.minute*60) + rt.Hora_refresh.second)) 
        if segundos > 21600:
            print(f'entrando em renovar com a data do mesmo dia {segundos}')
            resposta = Renovar()
            
            
    else:
        print(data_refresh,data_str)
        segundos = (86400 - ((rt.Hora_refresh.hour*3600) + (rt.Hora_refresh.minute*60) + rt.Hora_refresh.second)) + ((data_atual.hour*3600) + (data_atual.minute*60) + data_atual.second)
        if segundos > 21600:
            print(f'entrando em renovar com a data de dias diferentes {segundos}')
            resposta = Renovar()
            

    return HttpResponse(segundos)

def tratar_info(j_dict):
    
    
    attempts = j_dict['attempts']
    topico = j_dict['topic']

    print(f'entrei no tratar_info, attempts = {attempts}')
    print(f'topico = {topico}')
    if attempts == 1 :
        Tempo()
        print('acessando attempts 1')

        tabela_refresh = Access_token.objects.get(id=1)
    
        access_token = tabela_refresh.AC_token

        if topico == 'orders_v2':
            print('entrando em ordem_v2')

            id_venda = j_dict['resource'].split("/")[-1]
            (id_venda)
        
            url = f"https://api.mercadolibre.com/orders/{id_venda}"

            payload = {}
            headers = {
            'Authorization': f'Bearer {access_token}'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            print(response.text)
            j_dict = response.json()
            date_created = j_dict['date_created']
            data_obj = datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%S.%f%z")
            dia_compra = data_obj.day
            data_hora_atual = datetime.now()
            dia_atual = data_hora_atual.day

            if response.status_code == 200 and dia_atual == dia_compra :

                arquivo = response.json()
                id_compra = arquivo["id"]
                primeiro_item = arquivo["order_items"][0]["item"]
                id_anuncio = primeiro_item["id"]
                comprador = arquivo['buyer']
                date_created = arquivo['date_created']
                nickname = comprador['nickname']
                nome = comprador['first_name'] + " " + comprador['last_name']

                if id_anuncio == 'MLB2015443547':

                    url = f"https://api.mercadolibre.com/messages/packs/{id_compra}/sellers/34977269?tag=post_sale"

                    payload = {}
                    headers = {
                            'Authorization': f'Bearer {access_token}'
                    }

                    response = requests.request("GET", url, headers=headers, data=payload)

                    if response.status_code == 200:
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
                print(f'houve um erro ao tentar buscar a venda. Erro:{response.status_code}')


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
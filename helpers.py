import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from django.http import HttpResponse
from testeapp.models import Reflesh_Tokens,Access_token





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
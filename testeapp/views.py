import time
import os
import json
import requests
from dotenv import load_dotenv
from django.shortcuts import render
from helpers import Tempo
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from testeapp.models import Access_token



@csrf_exempt
def notifications(request):
    if request.method == 'POST':
        try:
            # Receber o JSON do corpo do pedido
            data = json.loads(request.body)
            print("JSON recebido:", data)
            # Fazer algo com os dados recebidos, se necessário

            # Responder com um JSON de confirmação e status 200 OK
            response_data = {"message": "Received and processed the JSON data successfully"}
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            # Se houver um erro ao analisar o JSON, responder com erro e status 400 Bad Request
            error_data = {"error": "Invalid JSON format"}
            return JsonResponse(error_data, status=400)
    else:
        # Responder com erro e status 405 Method Not Allowed se o método não for POST
        error_data = {"error": "Método não permitido"}
        return HttpResponse('Erro', status=500)
        #return JsonResponse(error_data, status=405)
   
 

def index(request):
   load_dotenv()
   CLIENT_ID = os.getenv("CLIENT_ID")
   CLIENT_SECRET = os.getenv("CLIENT_SECRET")
   REDIRECT_URI = os.getenv("REDIRECT_URI")

   
   return render(request, 'index.html')
   
def uri (request):
   return render(request, 'uri.html')


def items_post(request):

    try:
        #access_token = request.META.get('HTTP_ACCESS_TOKEN')
        #access_token = 'APP_USR-2417001236894079-081010-aaec5d1c2406664ec45fb0867b1b0058-34977269'
        #meli_object = MeliObject(access_token)
        Tempo()
        tabela_refresh = Access_token.objects.get(id=1)
    
        access_token = tabela_refresh.AC_token

        user_response = requests.get('https://api.mercadolibre.com/users/me', headers={'Authorization': f'Bearer {access_token}'})
        user = user_response.json()
        
        items_response = requests.get(f'https://api.mercadolibre.com/users/{user["id"]}/items/search', headers={'Authorization': f'Bearer {access_token}'})
        items = items_response.json().get('results', [])
       
        result = []
        for item_id in items:
            item_response = requests.get(f'https://api.mercadolibre.com/items/{item_id}', headers={'Authorization': f'Bearer {access_token}'})
            result.append(item_response.json())
         
         
        if result:
          
            return render(request, 'post.html', {'items': result})
        else:
            return HttpResponse('No items were found :(', status=404)
        
    except Exception as err:
        print('Something went wrong', err)
        return HttpResponse(f'Error! {err}', status=500)




   






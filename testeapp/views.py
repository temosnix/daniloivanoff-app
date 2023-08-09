from django.shortcuts import render
from dotenv import load_dotenv
import os
from django.http import HttpResponse
import requests



def index(request):
   load_dotenv()
   CLIENT_ID = os.getenv("CLIENT_ID")
   CLIENT_SECRET = os.getenv("CLIENT_SECRET")
   REDIRECT_URI = os.getenv("REDIRECT_URI")

   if CLIENT_ID == "3610569796440259":
      texto = "3610569796440259"
      return HttpResponse('certo')
   else:
      return HttpResponse('errado')

   





def listar_itens(request):
    
    try:
        # Supondo que você já tem o access_token disponível em res.locals.access_token
        access_token = request.res.locals['access_token']
        MeliObject = '0'
        # Criando o objeto MeliObject com o access_token
        meliObject = MeliObject(access_token)
        
        # Obtendo informações do usuário autenticado
        user_response = requests.get('https://api.mercadolibre.com/users/me', headers={'Authorization': f'Bearer {access_token}'})
        user = user_response.json()
        
        # Obtendo a lista de itens do usuário
        items_response = requests.get(f'https://api.mercadolibre.com/users/{user["id"]}/items/search', headers={'Authorization': f'Bearer {access_token}'})
        items = items_response.json().get('results', [])
        
        result = []
        for item_id in items:
            item_response = requests.get(f'https://api.mercadolibre.com/items/{item_id}', headers={'Authorization': f'Bearer {access_token}'})
            result.append(item_response.json())
        
        if result:
            return render(request, 'posts.html', {'items': result})
        else:
            return HttpResponse('No items were found :(', status=404)
        
    except Exception as err:
        print('Something went wrong', err)
        return HttpResponse(f'Error! {err}', status=500)

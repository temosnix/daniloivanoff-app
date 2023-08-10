from django.shortcuts import render
from dotenv import load_dotenv
import os
from django.http import HttpResponse
import requests


def notification (request):
    return render (request, 'notifications.html')

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
        access_token = 'APP_USR-2417001236894079-081010-aaec5d1c2406664ec45fb0867b1b0058-34977269'
        #meli_object = MeliObject(access_token)


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




   






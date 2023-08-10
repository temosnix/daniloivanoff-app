from django.shortcuts import render
from dotenv import load_dotenv
import os
from django.http import HttpResponse





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
   
def uri (request):
   return render(request, 'uri.html')


def notification(request):
   return render(request, 'notification.html')

   






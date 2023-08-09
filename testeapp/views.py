from django.shortcuts import render
from dotenv import load_dotenv
import os



def index(request):
   load_dotenv()
   CLIENT_ID = os.getenv("CLIENT_ID")
   CLIENT_SECRET = os.getenv("CLIENT_SECRET")
   REDIRECT_URI = os.getenv("REDIRECT_URI")

   
   return render (request, 'index.html') 



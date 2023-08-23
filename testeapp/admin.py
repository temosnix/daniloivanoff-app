from django.contrib import admin
from .models import Lojas, Access_token,Reflesh_Tokens,vendas_dfast

# Register your models here.

admin.site.register(Lojas)
admin.site.register(Access_token)
admin.site.register(Reflesh_Tokens)
admin.site.register(vendas_dfast)

from django.db import models


class Lojas(models.Model):
    Id_lojas = models.CharField(max_length=3)
    Nome = models.CharField(max_length=50)

    def __str__(self):
        return self.Nome
    
class Reflesh_Tokens (models.Model):
    lojas = models.OneToOneField(Lojas, on_delete=models.CASCADE)
    Id_refresh = models.CharField(max_length= 3)
    Rf_tokens = models.CharField(max_length=100)
    Hora_refresh = models.TimeField(auto_now_add=True)
    Data_refresh = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Rf_tokens
    
class Access_token(models.Model):
    lojas = models.OneToOneField(Lojas, on_delete=models.CASCADE)
    Id_access = models.CharField(max_length=3)
    AC_token = models.CharField(max_length=100)

    def __str__(self):
        return self.AC_token



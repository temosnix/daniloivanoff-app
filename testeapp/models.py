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

class vendas_dfast (models.Model):
    lojas = models.ForeignKey(Lojas,on_delete=models.CASCADE)
    Id_compra = models.CharField(max_length=30)
    Id_anuncio = models.CharField(max_length=30)
    Nome_cliente = models.CharField(max_length=50)
    Titulo = models.CharField(max_length=70)
    Data_compra = models.CharField(max_length=10)
    Quantidade = models.CharField(max_length=5)
    ENTREGUE_CHOICES = [
        ('true', 'Entregue'),
        ('false', 'Não Entregue'),
        ('null', 'Não Enviado'),
    ]
    Entregue = models.CharField(
        max_length=5,
        choices=ENTREGUE_CHOICES,
        default='null'
    )

    def __str__(self):
        return self.Id_compra



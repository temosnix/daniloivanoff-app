# Generated by Django 4.2.2 on 2023-08-16 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testeapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='vendas_dfast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Id_compra', models.CharField(max_length=30)),
                ('Id_anuncio', models.CharField(max_length=30)),
                ('Nome_cliente', models.CharField(max_length=50)),
                ('Titulo', models.CharField(max_length=70)),
                ('Data_compra', models.CharField(max_length=10)),
                ('Quantidade', models.CharField(max_length=5)),
                ('lojas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testeapp.lojas')),
            ],
        ),
    ]

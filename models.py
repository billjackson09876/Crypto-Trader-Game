from django.db import models

# Create your models here.

class Bank(models.Model):
	account_name = models.CharField(default = '', max_length=200)
	balance = models.DecimalField(max_digits=100, decimal_places=2)
	

class Coins(models.Model):
	coin_name = models.CharField(null=True, max_length=200)
	current_price = models.DecimalField(max_digits=12, decimal_places=2)
	market_cap = models.IntegerField(null= True, blank=True)
	high_24h = models.DecimalField(max_digits=12, decimal_places=2)
	low_24h = models.DecimalField(max_digits=12, decimal_places=2)

	class Meta:
		verbose_name_plural = 'coins'

class Asset(models.Model):
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
	asset = models.CharField(null=True, max_length=200)
	quantity = models.DecimalField(max_digits=12, decimal_places=2)
	current_price = models.DecimalField(max_digits=12, decimal_places=2)
	
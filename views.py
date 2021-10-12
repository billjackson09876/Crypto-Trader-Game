from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import requests
from .models import Coins, Bank, Asset
from .forms import TradeForm, SellForm

# Create your views here.

def index(request):
	return render(request, 'crypto_traders/index.html')

def coin_main(request):
	coins = Coins.objects.all()
	asset = Asset.objects.all()
	current_list = []
	for i in coins:
		current_list.append(i.coin_name)
	#use coingecko api for crypto listings
	url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
	response = requests.get(url)

	#save the response data
	coin_dict = response.json()



	for i in coin_dict[0:100]:
		if i.get('name') not in current_list:
			Coins.objects.create(coin_name=i.get("name"), 
				current_price=i.get('current_price'),
				market_cap=i.get('market_cap'), 
				high_24h=i.get('high_24h'),
				low_24h=i.get('low_24h')
				)


	for coin in coins:
		for i in coin_dict[0:100]:
			if i.get('name') in coin.coin_name:
				coin.current_price = i.get('current_price')
				coin.market_cap = i.get('market_cap')
				coin.high_24h = i.get('high_24h')
				coin.low_24h = i.get('low_24h')
				coin.save()

	#create html table
	overall = '<th>Coin</th><th>Price</th><th>Market Cap</th><th>24h High</th><th>24h Low</th><th colspan="2">Trade</th>'

	for i in coins:

		name = i.coin_name
		current_price = "{:,}".format(i.current_price)
		market_cap = "{:,}".format(i.market_cap)
		high_24h = "{:,}".format(i.high_24h)
		low_24h = "{:,}".format(i.low_24h)

		overall += f'<tr>'
		overall += f'<td><a href="/coin_main/{i.id}">{name}</a></td>'
		overall += f'<td>{current_price}</td>'
		overall += f'<td>{market_cap}</td>'
		overall += f'<td>{high_24h}</td>'
		overall += f'<td>{low_24h}</td>'
		overall += f'<td><a href="/coin_main/{i.id}/buy">Buy</a></td>'
		overall += f'<td><a href="/coin_main/{i.id}/sell">Sell</a></td>'
		overall += f'</tr>'

	table = f'<table>{overall}</table>'

	context = {'table': mark_safe(table), 'coins': coins}

	return render(request, 'crypto_traders/coin_main.html', context)

def individual_coin(request, coins_id):
	coins = Coins.objects.get(id=coins_id)
	overall = '<th>Coin</th><th>Price</th><th>Market Cap</th><th>24h High</th><th>24h Low</th>'

	name = coins.coin_name
	current_price = "{:,}".format(coins.current_price)
	market_cap = "{:,}".format(coins.market_cap)
	high_24h = "{:,}".format(coins.high_24h)
	low_24h = "{:,}".format(coins.low_24h)

	overall += f'<tr>'
	overall += f'<td>{name}</td>'
	overall += f'<td>{current_price}</td>'
	overall += f'<td>{market_cap}</td>'
	overall += f'<td>{high_24h}</td>'
	overall += f'<td>{low_24h}</td>'
	overall += f'</tr>'

	table = f'<table>{overall}</table>'
	
	context = {'table': mark_safe(table)}

	return render(request, 'crypto_traders/individual_coin.html', context)

def portfolio(request):
	bank = Bank.objects.all()
	assets = Asset.objects.all()
	overall = '<th>Account Name</th><th>Balance</th>'
	overall2 = '<th>Asset</th><th>Quantity</th><th>Price</th><th>Total Value</th>'
	
	url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
	response = requests.get(url)
	coin_dict = response.json()

	total_exp = 0

	for asset in assets:
		for i in coin_dict[0:100]:
			if i.get('name') in asset.asset:
				asset.current_price = i.get('current_price')
				asset.save()

	for i in assets:
		if i.quantity == 0:
			i.delete()

		name = i.asset
		quantity = "{:,}".format(i.quantity)
		current_price = "{:,}".format(i.current_price)
		total = "{:,}".format(float(i.quantity) * i.current_price)

		overall2 += f'<tr>'
		overall2 += f'<td>{name}</td>'
		overall2 += f'<td>{quantity}</td>'
		overall2 += f'<td>{current_price}</td>'
		overall2 += f'<td>{total}</td>'
		overall2 += f'</tr>'

		total_exp += round(float(i.quantity) * (i.current_price),2)

	for i in bank:
		name = i.account_name

		balance = "{:,}".format(i.balance)

		overall += f'<tr>'
		overall += f'<td>{name}</td>'
		overall += f'<td>{balance}</td>'
		overall += f'</tr>'
	
		

	table = f'<table>{overall}</table>'	
	table2 = f'<table>{overall2}</table>'	
	context = {'table': mark_safe(table), 'table2': mark_safe(table2)}

	return render(request, 'crypto_traders/portfolio.html', context)

def buy(request, coins_id):
	coins = Coins.objects.get(id=coins_id)
	banks = Bank.objects.get(id=1)
	assets = Asset.objects.all()

	total_assets = []
	for coin in assets:
		total_assets.append(coin.asset)

	overall = '<th>Coin</th><th>Price</th><th>Market Cap</th><th>24h High</th><th>24h Low</th>'

	name = coins.coin_name
	current_price = "{:,}".format(coins.current_price)
	market_cap = "{:,}".format(coins.market_cap)
	high_24h = "{:,}".format(coins.high_24h)
	low_24h = "{:,}".format(coins.low_24h)

	overall += f'<tr>'
	overall += f'<td>{name}</td>'
	overall += f'<td>{current_price}</td>'
	overall += f'<td>{market_cap}</td>'
	overall += f'<td>{high_24h}</td>'
	overall += f'<td>{low_24h}</td>'
	overall += f'</tr>'

	table = f'<table>{overall}</table>'
	x = 1
	if request.method != 'POST':
		form = TradeForm()
	else:
		if coins.coin_name not in total_assets:
			form = TradeForm(data=request.POST)
			if form.is_valid():
				new_coin = form.save(commit=False)
				new_coin.asset = coins.coin_name
				new_coin.bank = banks
				new_coin.current_price = coins.current_price
				total_cost = coins.current_price * new_coin.quantity
				if total_cost < banks.balance:
					x = 1
					banks.balance -= coins.current_price * new_coin.quantity
					banks.save()
					new_coin.save()
					return redirect('crypto_traders:portfolio')
				else:
					x = 0

					
				
		else:
			for i in assets:
				if i.asset == coins.coin_name:
					inst = i
					old_quantity = i.quantity
			form = TradeForm(data=request.POST, instance=inst)
			if form.is_valid():
				old_coin = form.save(commit=False)
				old_coin.asset = coins.coin_name
				old_coin.bank = banks
				old_coin.current_price = coins.current_price
				for i in assets:
					if i.asset == coins.coin_name:
						old_coin.quantity += old_quantity
				total_price = coins.current_price * old_coin.quantity
				if total_price < banks.balance:
					x = 1
					banks.balance -= coins.current_price * old_coin.quantity
					banks.save()
					old_coin.save()
					return redirect('crypto_traders:portfolio')
				else:
					x = 0

	context = {'table': mark_safe(table), 'form': form, 'x': x}

	return render(request, 'crypto_traders/buy.html', context)

def sell(request, coins_id):
	coins = Coins.objects.get(id=coins_id)
	banks = Bank.objects.get(id=1)
	assets = Asset.objects.all()

	total_assets = []
	for coin in assets:
		total_assets.append(coin.asset)

	overall = '<th>Coin</th><th>Price</th><th>Market Cap</th><th>24h High</th><th>24h Low</th>'

	name = coins.coin_name
	current_price = "{:,}".format(coins.current_price)
	market_cap = "{:,}".format(coins.market_cap)
	high_24h = "{:,}".format(coins.high_24h)
	low_24h = "{:,}".format(coins.low_24h)

	overall += f'<tr>'
	overall += f'<td>{name}</td>'
	overall += f'<td>{current_price}</td>'
	overall += f'<td>{market_cap}</td>'
	overall += f'<td>{high_24h}</td>'
	overall += f'<td>{low_24h}</td>'
	overall += f'</tr>'

	table = f'<table>{overall}</table>'
	x = 1
	message = ''
	if request.method != 'POST':
		if coins.coin_name not in total_assets:
			message = 'You do not own any of this coin'
			form = TradeForm()
			form.fields['quantity'].disabled = True
		else:
			form = TradeForm()
			
	else:
		for i in assets:
			if i.asset == coins.coin_name:
				inst = i
				old_quantity = i.quantity
		form = TradeForm(data=request.POST, instance=inst)
		if form.is_valid():
			old_coin = form.save(commit=False)
			old_coin.asset = coins.coin_name
			old_coin.bank = banks
			old_coin.current_price = coins.current_price
			if old_coin.quantity <= old_quantity:
				x = 1
				banks.balance += coins.current_price * old_coin.quantity
				old_coin.quantity = (old_quantity - old_coin.quantity)
				banks.save()
				old_coin.save()
				return redirect('crypto_traders:portfolio')
			else:
				x = 0

	context = {'table': mark_safe(table), 'form': form, 'x': x, 'message': message}

	return render(request, 'crypto_traders/sell.html', context)



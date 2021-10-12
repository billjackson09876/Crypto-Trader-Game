from django.urls import path

from . import views

app_name = 'crypto_traders'
urlpatterns = [
	path('', views.index, name='index'),
	path('coin_main', views.coin_main, name='coin_main'),
	path('coin_main/<int:coins_id>/', views.individual_coin, name='individual_coin'),
	path('coin_main/<int:coins_id>/buy', views.buy, name='buy'),
	path('coin_main/<int:coins_id>/sell', views.sell, name='sell'),
	path('portfolio/', views.portfolio, name='portfolio'),


]
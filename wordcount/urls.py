from django.urls import path
from . import views

app_name = 'wordcount'
urlpatterns = [
    path('', views.frequency, name='frequency'),
    path('frequency', views.frequency, name='frequency'),
    path('search', views.search, name='search'),
    path('result/<payload>/<db_status>', views.result, name='result')
]
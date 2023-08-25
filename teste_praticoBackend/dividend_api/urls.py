from django.urls import path
from .views import dividend_summary

urlpatterns = [
    path('dividend-summary/', dividend_summary, name='dividend-summary'),
]
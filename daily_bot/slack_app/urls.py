from django.urls import path
from . import views

urlpatterns = [
    path('interaction/', views.Interaction.as_view(), name='interaction'),
    path('events/', views.Events.as_view(), name='events'),
    path('fetch_channels/', views.FetchChannels.as_view(), name='fetch_channels'),
    path('test/', views.Test.as_view(), name='test'),
]

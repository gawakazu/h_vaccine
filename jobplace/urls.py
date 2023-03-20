from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import LoginView,LogoutView,MainView,PlaceView,DateView,TimeView,ConfirmView,Place2View,Date2View

urlpatterns = [
    path('',LoginView.as_view(),name='login'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('main/',MainView.as_view(),name='main'),
    path('place/',PlaceView.as_view(),name='place'),
    path('date/<str:i>',DateView.as_view(),name='date'),
    path('date2/<str:place><str:previous_month>',Date2View.as_view(),name='date2'),
    path('time/<str:place><str:i>',TimeView.as_view(),name='time'),
    path('place2/<str:select><str:i>',Place2View.as_view(),name='place2'),
    path('confirm/<str:select><str:i>',ConfirmView.as_view(),name='confirm'),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

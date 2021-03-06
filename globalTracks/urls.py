"""novcov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('status', views.Global.as_view(), name='global_status'),
    path('maps', views.Map.as_view(),name='global_map'),
    path('update-data', views.DataUpdate.as_view(),name='Global_data_update'),
    # path('State-chart', views.SateCharts.as_view() , name="state_chart"),
    path('news', views.News.as_view() , name="global_news"),

]

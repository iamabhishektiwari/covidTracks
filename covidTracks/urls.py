"""covidTracks URL Configuration

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
from django.urls import path,include
from globalTracks import views as gv
from indiaTracks import views as iv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('global/', include('globalTracks.urls')),
    path('india/', include('indiaTracks.urls')),
    path('about-covid19', gv.Covid.as_view(),name='about_covid19'),
    path('', iv.India.as_view(),name='HomePage')
]

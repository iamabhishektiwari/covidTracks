from .models import Country, Province, City, ImpParam
import time
from django.db.models import Sum
import requests





def fetchData():
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
    querystring = {"country":"Canada"}
    headers = {
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
        'x-rapidapi-key': "78144a9bd9msh16e7e3bc08ebff0p1d5199jsn8b8bdd31763d"
        }

    page = requests.request("GET", url, headers=headers).json()#, params=querystring)
    if(page['error']== False and page['statusCode']==200):
        datas = page['data']['covid19Stats']
        for data in datas:
            city = data['city']
            province = data['province']
            country = data['country']
            lastupdate = data['lastUpdate']
            keyid = data['keyId']
            confirmed = data['confirmed']
            recovered = data['recovered']
            deaths = data['deaths']


            try:
                cn = Country.objects.get(name=country)
                cn.lastupdate = lastupdate
                if(city=="" and province ==""):
                    cn.totaldeaths = deaths
                    cn.totalconfirmed = confirmed
                    cn.totalrecovered = recovered
                else:
                    cn.totaldeaths = 0
                    cn.totalconfirmed = 0
                    cn.totalrecovered = 0

                cn.save()
            except Exception as e:
                cn = Country(name=country,
                             latitude=0,
                             longitude=0,
                             lastupdate=lastupdate);
                if(city=="" and province ==""):
                    cn.totaldeaths = deaths
                    cn.totalconfirmed = confirmed
                    cn.totalrecovered = recovered
                else:
                    cn.totaldeaths = 0
                    cn.totalconfirmed = 0
                    cn.totalrecovered = 0
                cn.save()

            try:
                cn = Country.objects.get(name=country)
                pn = Province.objects.get(name=province,country=cn)
                if(city=="" and province != ""):
                    pn.totaldeaths = deaths
                    pn.totalconfirmed = confirmed
                    pn.totalrecovered = recovered
                pn.save()
            except Exception as e:
                if(province!=""):

                    cn = Country.objects.get(name=country)
                    pn = Province(name=province,
                                  latitude=0,
                                  longitude=0,
                                  country=cn)
                    if(city=="" and province != ""):
                        pn.totaldeaths = deaths
                        pn.totalconfirmed = confirmed
                        pn.totalrecovered = recovered
                    pn.save()

            try:
                cn = Country.objects.get(name=country)
                pn = Province.objects.get(name=province)
                ci = City.objects.get(name=city,country=cn,province=pn)
                ci.totaldeaths = deaths
                ci.totalconfirmed = confirmed
                ci.totalrecovered = recovered

                ci.save()
            except Exception as e:
                if(city!=""):
                    cn = Country.objects.get(name=country)
                    pn = Province.objects.get(name=province)
                    ci = City(name=city,
                              totaldeaths=deaths,
                              totalconfirmed=confirmed,
                              totalrecovered=recovered,
                              latitude=0,
                              longitude=0,
                              keyid=keyid,
                              province=pn,
                              country=cn)
                    ci.save()



def InternalCalculations():
    provinces = Province.objects.all()
    countries = Country.objects.all()

    for pn in provinces:
        if(City.objects.all().filter(province=pn).exists()):
            pn.totalconfirmed = City.objects.all().filter(province=pn).aggregate(Sum('totalconfirmed'))['totalconfirmed__sum']
            pn.totalrecovered = City.objects.all().filter(province=pn).aggregate(Sum('totalrecovered'))['totalrecovered__sum']
            pn.totaldeaths =    City.objects.all().filter(province=pn).aggregate(Sum('totaldeaths'))['totaldeaths__sum']
            pn.save()
    for con in countries:
        if(Province.objects.all().filter(country=con)):
            con.totalconfirmed = con.totalconfirmed+Province.objects.all().filter(country=con).aggregate(Sum('totalconfirmed'))['totalconfirmed__sum']
            con.totalrecovered = con.totalrecovered+Province.objects.all().filter(country=con).aggregate(Sum('totalrecovered'))['totalrecovered__sum']
            con.totaldeaths    = con.totaldeaths+Province.objects.all().filter(country=con).aggregate(Sum('totaldeaths'))['totaldeaths__sum']
            con.save()

def GlobalTotalCalc():
    try:
        tc = ImpParam.objects.get(key="totalconfirmed")
        tr = ImpParam.objects.get(key="totalrecovered")
        td = ImpParam.objects.get(key="totaldeaths")
        tc.value = Country.objects.all().aggregate(Sum('totalconfirmed'))['totalconfirmed__sum']
        tr.value = Country.objects.all().aggregate(Sum('totalrecovered'))['totalrecovered__sum']
        td.value = Country.objects.all().aggregate(Sum('totaldeaths'))['totaldeaths__sum']

        tc.save()
        tr.save()
        td.save()

    except Exception as e:
        tc = ImpParam(key="totalconfirmed",value=Country.objects.all().aggregate(Sum('totalconfirmed'))['totalconfirmed__sum'])
        tr = ImpParam(key="totalrecovered",value=Country.objects.all().aggregate(Sum('totalrecovered'))['totalrecovered__sum'])
        td = ImpParam(key="totaldeaths",value=Country.objects.all().aggregate(Sum('totaldeaths'))['totaldeaths__sum'])

        tc.save()
        tr.save()
        td.save()

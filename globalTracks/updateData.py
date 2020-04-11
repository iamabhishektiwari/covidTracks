from .models import Country, Province, City, ImpParam
import time
from django.db.models import Sum
import requests
import json
import os
THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


dateinfo = ['1-22-20','1-23-20','1-24-20','1-25-20','1-26-20',
            '1-27-20','1-28-20','1-29-20','1-30-20','1-31-20',
            '2-1-20','2-2-20','2-3-20', '2-4-20','2-5-20',
            '2-6-20','2-7-20', '2-8-20', '2-9-20', '2-10-20',
            '2-11-20', '2-12-20', '2-13-20', '2-14-20', '2-15-20',
            '2-16-20', '2-17-20', '2-18-20', '2-19-20', '2-20-20',
            '2-21-20', '2-22-20', '2-23-20', '2-24-20', '2-25-20',
            '2-26-20', '2-27-20', '2-28-20', '2-29-20', '3-1-20',
            '3-2-20', '3-3-20', '3-4-20', '3-5-20', '3-6-20',
            '3-7-20', '3-8-20', '3-9-20', '3-10-20', '3-11-20',
            '3-12-20', '3-13-20', '3-14-20', '3-15-20', '3-16-20',
            '3-17-20', '3-18-20', '3-19-20', '3-20-20', '3-21-20',
            '3-22-20', '3-23-20', '3-24-20', '3-25-20', '3-26-20',
            '3-27-20', '3-28-20', '3-29-20', '3-30-20', '3-31-20',
            '4-1-20', '4-2-20', '4-3-20', '4-4-20', '4-5-20',
            '4-6-20', '4-7-20', '4-8-20', '4-9-20']

def fetchData():
    print("###################################################")
    print("Updating Global Data")
    print("###################################################")
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



def globalTimeSeries():
    print("###################################################")
    print("Updating Global Timeseries")
    print("###################################################")
    url = "https://covid19-india-data.herokuapp.com/GlobalTimeSeries"
    page = requests.get(url).json()
    my_file = os.path.join(THIS_FOLDER, 'helper_data/globaltimeseries.json')
    with open(my_file, 'w') as outfile:
        json.dump(page, outfile)





def SaveRenderTimeSeriesData(countries):
    page = {}
    my_file = os.path.join(THIS_FOLDER, 'helper_data/globaltimeseries.json')
    with open(my_file, "r") as read_file:
        page = json.load(read_file)
    rowdata = []
    i=1;
    for day in dateinfo:
        tmpls = [i]
        i = i+1
        for country in countries:
            tmpls.append(page[country.name]['data'][day]['confirm'])
        rowdata.append(tmpls);
    return rowdata



def smallGraph(country):
    page = {}
    my_file = os.path.join(THIS_FOLDER, 'helper_data/globaltimeseries.json')
    with open(my_file, "r") as read_file:
        page = json.load(read_file)
    rowdata = []
    i =1
    for day in dateinfo:
        rowdata.append([i,
                        page[country.name]['data'][day]['confirm'],
                        page[country.name]['data'][day]['deaths'],
                        page[country.name]['data'][day]['recovered']])
        i = i+1
    return rowdata

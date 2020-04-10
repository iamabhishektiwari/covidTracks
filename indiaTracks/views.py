from django.shortcuts import render
from django.views.generic import View
import requests
from .models import States, ImpParam
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import time
import json
from getNews import NewsFromApi
# Create your views here.








def fetchData():
    url = "https://covid19-india-data.herokuapp.com/getStateData"
    page = requests.get(url).json()
    data = page['data']
    record_update_time = page['update-time']

    totaldeaths = 0;
    totalconfirmed = 0;
    totalrecovered = 0;

    for key in data:

        try:
            pk = States.objects.get(name=key)
            pk = States.objects.get(name=key)
            pk.totalconfirmed = data[key]['Confirmed Cases']
            pk.totaldeaths = data[key]['Deaths']
            pk.totalrecovered = data[key]['Cured/Discharged']
            pk.save()
        except Exception as e:
            pk = States(name=key,
                        totalconfirmed=int(data[key]['Confirmed Cases']),
                        totaldeaths = int(data[key]['Deaths']),
                        totalrecovered = int(data[key]['Cured/Discharged']),
                        latitude=0,
                        longitude=0);
            pk.save()

        totaldeaths = totaldeaths+int(data[key]['Deaths'])
        totalconfirmed = totalconfirmed+int(data[key]['Confirmed Cases'])
        totalrecovered = totalrecovered+int(data[key]['Cured/Discharged'])


        try:
            rut = ImpParam.objects.get(key='record_update_time')

            param1 = ImpParam.objects.get(key='totaldeaths')
            param2 = ImpParam.objects.get(key='totalconfirmed')
            param3 = ImpParam.objects.get(key='totalrecovered')

            rut.value = record_update_time
            rut.save()

            param1.value = totaldeaths
            param2.value = totalconfirmed
            param3.value = totalrecovered

            param1.save()
            param2.save()
            param3.save()

        except Exception as e:

            rut = ImpParam(key='record_update_time',value=record_update_time)
            param1 = ImpParam(key='totaldeaths',value=totaldeaths)
            param2 = ImpParam(key='totalconfirmed',value=totalconfirmed)
            param3 = ImpParam(key='totalrecovered',value=totalrecovered)

            rut.save()
            param1.save()
            param2.save()
            param3.save()






class India(View):
    update_time = ImpParam.objects.get(key='update_time');
    if(float(update_time.value)+3600 < time.time()):
        update_time.value = time.time()
        update_time.save()
        fetchData()
    mytemplate = 'india_status.html'
    unsupported = 'Unsupported operation'
    stateinfo = {}
    with open('helper_data/stateinfo.json', 'r') as openfile:
        stateinfo = json.load(openfile)
    def get(self, request):

        totalconfirmed = ImpParam.objects.get(key='totalconfirmed').value
        totalrecovered = ImpParam.objects.get(key='totalrecovered').value
        totaldeaths = ImpParam.objects.get(key='totaldeaths').value

        # r = Region.objects.get(name='India')
        # subregions = SubRegion.objects.all().filter(region=r).order_by('-totalconfirmed')
        states = States.objects.all().order_by('-totalconfirmed')
        retlist = [["State Code", "State", "Number"],];

        for state in states:
            state_code = self.stateinfo['statecode'][state.name]
            State = state.name
            number = state.totalconfirmed

            retlist.append([state_code,State,number])
        #
        # totaldeaths    = Region.objects.get(name='India').totaldeaths
        # totalrecovered = Region.objects.get(name='India').totalrecovered
        # totalconfirmed = Region.objects.get(name='India').totalconfirmed
        # chart_data = [['State', 'Total Confirmed', 'Recovered']]
        # for rs in subregions:
        #     if(rs.totalconfirmed>0):
        #         chart_data.append([rs.name,rs.totalconfirmed,rs.totalrecovered])
        #         ls = [self.statecode[rs.name],rs.name,rs.totalconfirmed]
        #         retlist.append(ls)
        #
        #
        #
        context = {
            'states':states,
            'retlist':retlist,
            'totalconfirmed':totalconfirmed,
            'totalrecovered':totalrecovered,
            'totaldeaths':totaldeaths,
            'phoneno':self.stateinfo['phoneno'],
        }
        return render(request,self.mytemplate,context=context)

    def post(self, request):
        return HttpResponse(self.unsupported)



class News(View):

    mytemplate = 'news.html'
    unsupported = 'Unsupported operation'

    def get(self, request):
        date_ ="from="+str(datetime.now().date())+"&"
        url = ('http://newsapi.org/v2/top-headlines?'
                'country=in&'
                'q=coronavirus&'+
                date_+
               'sortBy=popularity&'
               'apiKey=55d55abffe3c48298169fd84576a8d48')
        news = NewsFromApi(url)

        context = {
        'news':news,
        'Region':"India"
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)

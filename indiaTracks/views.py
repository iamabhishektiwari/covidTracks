from django.shortcuts import render
from django.views.generic import View
import requests
from .models import States, ImpParam, State_k, District
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import time
import json
from getNews import NewsFromApi
from .updateData import fetchData, findDataSample2
import os
import random
# Create your views here.
THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

my_file = os.path.join(THIS_FOLDER, 'helper_data/stateinfo.json')
stateinfo = {}
with open(my_file, 'r') as openfile:
    stateinfo = json.load(openfile)


class DataUpdate(View):
    mytemplate = 'update_data_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        fetchData()
        findDataSample2()

        context = {
            'message':"Success",
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)


class Helpline(View):

    mytemplate = 'helpline.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        context = {
            'phoneno':stateinfo['phoneno'],
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)




class Map(View):
    mytemplate = 'india_maps.html'
    unsupported = 'Unsupported operation'

    def get(self, request):

        totalconfirmed = ImpParam.objects.get(key='totalconfirmed').value
        totalrecovered = ImpParam.objects.get(key='totalrecovered').value
        totaldeaths = ImpParam.objects.get(key='totaldeaths').value


        states = States.objects.all().order_by('-totalconfirmed')
        retlist = [["State Code", "State", "Number"],];

        for state in states:
            state_code = stateinfo['statecode'][state.name]
            State = state.name
            number = state.totalconfirmed

            retlist.append([state_code,State,number])

        context = {
            'states':states,
            'retlist':retlist,
            'totalconfirmed':totalconfirmed,
            'totalrecovered':totalrecovered,
            'totaldeaths':totaldeaths,
        }
        return render(request,self.mytemplate,context=context)

    def post(self, request):
        return HttpResponse(self.unsupported)





class India(View):

    mytemplate = 'india_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        record_update_time = ImpParam.objects.get(key='record_update_time').value
        nongov_lastupdate = ImpParam.objects.get(key='nongov_lastupdate').value

        totalconfirmed = ImpParam.objects.get(key='totalconfirmed').value
        totalrecovered = ImpParam.objects.get(key='totalrecovered').value
        totaldeaths = ImpParam.objects.get(key='totaldeaths').value
        totalactive = int(totalconfirmed) - int(totaldeaths)-int(totalrecovered)-1;

        # r = Region.objects.get(name='India')
        # subregions = SubRegion.objects.all().filter(region=r).order_by('-totalconfirmed')
        states = States.objects.all().order_by('-totalconfirmed')

        StateDistrict = {}

        statek = State_k.objects.all().filter(confirmed__gte=1).order_by('-confirmed')
        for ss in statek:
            dists = District.objects.all().filter(state=ss).order_by('-confirmed')
            StateDistrict[ss] = dists



        nongov_totalconfirmed = ImpParam.objects.get(key='nongov_totalconfirmed').value
        nongov_totalrecovered = ImpParam.objects.get(key='nongov_totalrecovered').value
        nongov_totaldeaths = ImpParam.objects.get(key='nongov_totaldeaths').value
        nongov_active = ImpParam.objects.get(key='nongov_active').value
        nongov_deltaconfirmed = ImpParam.objects.get(key='nongov_deltaconfirmed').value

        fake_update = random.randint(0,30);



        context = {
            'states':states,
            'totalconfirmed':totalconfirmed,
            'totalrecovered':totalrecovered,
            'totaldeaths':totaldeaths,
            'phoneno':stateinfo['phoneno'],
            'StateDistrict':StateDistrict,
            'record_update_time':record_update_time,
            'nongov_totalconfirmed':nongov_totalconfirmed,
            'nongov_totalrecovered':nongov_totalrecovered,
            'nongov_totaldeaths':nongov_totaldeaths,
            'nongov_active':nongov_active,
            'nongov_deltaconfirmed':nongov_deltaconfirmed,
            'nongov_lastupdate':nongov_lastupdate,
            'totalactive':totalactive,
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

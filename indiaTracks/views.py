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
# Create your views here.



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
    stateinfo = {}
    with open('helper_data/stateinfo.json', 'r') as openfile:
        stateinfo = json.load(openfile)
    mytemplate = 'helpline.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        context = {
            'phoneno':self.stateinfo['phoneno'],
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)




class Map(View):
    mytemplate = 'india_maps.html'
    unsupported = 'Unsupported operation'
    stateinfo = {}
    with open('helper_data/stateinfo.json', 'r') as openfile:
        stateinfo = json.load(openfile)
    def get(self, request):

        totalconfirmed = ImpParam.objects.get(key='totalconfirmed').value
        totalrecovered = ImpParam.objects.get(key='totalrecovered').value
        totaldeaths = ImpParam.objects.get(key='totaldeaths').value


        states = States.objects.all().order_by('-totalconfirmed')
        retlist = [["State Code", "State", "Number"],];

        for state in states:
            state_code = self.stateinfo['statecode'][state.name]
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

    record_update_time = ImpParam.objects.get(key='record_update_time').value
    nongov_lastupdate = ImpParam.objects.get(key='nongov_lastupdate').value
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




        context = {
            'states':states,
            'totalconfirmed':totalconfirmed,
            'totalrecovered':totalrecovered,
            'totaldeaths':totaldeaths,
            'phoneno':self.stateinfo['phoneno'],
            'StateDistrict':StateDistrict,
            'record_update_time':self.record_update_time,
            'nongov_totalconfirmed':nongov_totalconfirmed,
            'nongov_totalrecovered':nongov_totalrecovered,
            'nongov_totaldeaths':nongov_totaldeaths,
            'nongov_active':nongov_active,
            'nongov_deltaconfirmed':nongov_deltaconfirmed,
            'nongov_lastupdate':self.nongov_lastupdate,
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

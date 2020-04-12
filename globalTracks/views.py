from django.shortcuts import render
from django.views.generic import View
import requests
from .models import Country, Province, City, ImpParam
import time
from django.db.models import Sum
from .updateData import fetchData, InternalCalculations, GlobalTotalCalc, smallGraph, globalTimeSeries,SaveRenderTimeSeriesData
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime
from getNews import NewsFromApi
# Create your views here.




class Covid(View):
    mytemplate = 'covid19.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        context = {

        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)

class DataUpdate(View):
    mytemplate = 'update_data_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        fetchData()
        InternalCalculations()
        GlobalTotalCalc()
        globalTimeSeries()

        context = {
            'message':"Success",
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)



class Global(View):

    mytemplate = 'global_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        regions = Country.objects.all().order_by('-totalconfirmed')
        totaldeaths =    ImpParam.objects.get(key='totaldeaths').value
        totalrecovered = ImpParam.objects.get(key='totalrecovered').value
        totalconfirmed = ImpParam.objects.get(key='totalconfirmed').value
        subregionlist = {}

        for region in regions:
            subregs = Province.objects.all().filter(country=region).order_by('-totalconfirmed')
            if subregs:
                x = {region:subregs}
                subregionlist.update(x)



        context = {
            'regions':regions,
            'totalconfirmed':totalconfirmed,
            'totalrecovered':totalrecovered,
            'totaldeaths':totaldeaths,
            'subregionlist':subregionlist,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)


class Map(View):
    mytemplate = 'global_maps.html'
    unsupported = 'Unsupported operation'
    top4 = Country.objects.all().order_by('-totalconfirmed')[0:4]
    rowdata1 = smallGraph(top4[0])
    rowdata2 = smallGraph(top4[1])
    rowdata3 = smallGraph(top4[2])
    rowdata4 = smallGraph(top4[3])
    def get(self, request):

        regions = Country.objects.all().order_by('-totalconfirmed')
        totaldeaths    = ImpParam.objects.get(key='totaldeaths').value
        totalrecovered = ImpParam.objects.get(key='totalrecovered').value
        totalconfirmed = ImpParam.objects.get(key='totalconfirmed').value
        regions_list = [];
        graph_data = [['Country', 'Cases']]



        for region in regions:
            graph_data.append([region.name, region.totalconfirmed])
            prov = Province.objects.all().filter(country=region)
            if(prov):
                regions_list.append(region)
        options = {
            'colorAxis': {'colors': ['pink', 'red']}
            };
        context = {
            'totalconfirmed':totalconfirmed,
            'totalrecovered':totalrecovered,
            'totaldeaths':totaldeaths,
            'api_key':'AIzaSyDq89_RotaPqH4iohtHOI8udn6TuIMlWdA',
            'regions':regions_list,
            'activefor':"Global",
            'graph_data':graph_data,
            'options':options,
            'top1':self.top4[0],
            'top2':self.top4[1],
            'top3':self.top4[2],
            'top4':self.top4[3],
            'rowdata1':self.rowdata1,
            'rowdata2':self.rowdata2,
            'rowdata3':self.rowdata3,
            'rowdata4':self.rowdata4,
        }
        return render(request,self.mytemplate,context)



    def post(self, request):

        country = request.POST.get('named')
        if country == "Global":
            return HttpResponseRedirect(self.request.path_info)

        queryregion = Country.objects.get(name=country)
        subregions = Province.objects.all().filter(country=queryregion).order_by('-totalconfirmed')

        graph_data = [['provinces', 'Cases']]
        if(subregions):
            for subreg in subregions:
                graph_data.append([subreg.name, subreg.totalconfirmed ])
        else:
            graph_data.append([queryregion.name, queryregion.totalconfirmed ])

        totaldeaths =    ImpParam.objects.get(key='totaldeaths').value
        totalrecovered = ImpParam.objects.get(key='totalrecovered').value
        totalconfirmed = ImpParam.objects.get(key='totalconfirmed').value

        regions = Country.objects.all().order_by('-totalconfirmed')
        regions_list = [];
        for region in regions:
            prov = Province.objects.all().filter(country=region)
            if(prov):
                regions_list.append(region)

        country_code_dict = {'US':'US',
                             'France':'FR',
                             'China':'CN',
                             'United Kingdom':'GB',
                             'Netherlands':'NL',
                             'Canada':'CA',
                             'Australia':'AU',
                             'Denmark':'DK'
                             }
        if(country == 'US' or country == 'Canada' or country =='Australia'):
            options = {
                'region': country_code_dict[country],
                'displayMode': 'regions',
                'resolution': 'provinces',
                'colorAxis': {'colors': ['pink', 'red']}
                };
        else:
            options = {
                'region': country_code_dict[country],
                'displayMode': 'regions',
                'colorAxis': {'colors': ['pink', 'red']}
                };
            graph_data.append([queryregion.name, queryregion.totalconfirmed])
        context = {
            'totalconfirmed':totalconfirmed,
            'totalrecovered':totalrecovered,
            'totaldeaths':totaldeaths,
            'api_key':'AIzaSyDq89_RotaPqH4iohtHOI8udn6TuIMlWdA',
            'regions':regions_list,
            'activefor':country,
            'graph_data':graph_data,
            'options':options,
            'top1':self.top4[0],
            'top2':self.top4[1],
            'top3':self.top4[2],
            'top4':self.top4[3],
            'rowdata1':self.rowdata1,
            'rowdata2':self.rowdata2,
            'rowdata3':self.rowdata3,
            'rowdata4':self.rowdata4,
        }
        print(graph_data)
        return render(request,self.mytemplate,context)



class News(View):

    mytemplate = 'news.html'
    unsupported = 'Unsupported operation'

    def get(self, request):
        date_ ="from="+str(datetime.now().date())+"&"
        url = ('http://newsapi.org/v2/everything?'
               'q=Covid19&'+
               date_+
               'sortBy=popularity&'
               'apiKey=55d55abffe3c48298169fd84576a8d48')
        news = NewsFromApi(url)

        context = {
        'news':news,
        'Region':"Global"
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)

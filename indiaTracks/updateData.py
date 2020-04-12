from .models import States, ImpParam, State_k, District
import json
import requests

def fetchData():
    print("###################################################")
    print("Filling MOH Data")
    print("###################################################")
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


def findDataSample2():
    print("###################################################")
    print("Filling District Data")
    print("###################################################")
    url = "https://covid19-india-data.herokuapp.com/getDistrictData"
    page = requests.get(url).json()
    data = page['state_wise']
    nongov = page['total_values']
    for stname in data:
        try:
            stk = State_k.objects.get(name=stname)
            stk.confirmed = data[stname]['confirmed']
            stk.active = data[stname]['active']
            stk.deaths = data[stname]['deaths']
            stk.recovered = data[stname]['recovered']
            stk.deltaDeaths = data[stname]['deltadeaths']
            stk.deltaRecovered= data[stname]['deltarecovered']
            stk.deltaConfirmed= data[stname]['deltaconfirmed']
            stk.lastupdate = data[stname]['lastupdatedtime']

            stk.save()
        except Exception as e:
            stk = State_k(name=stname,
                          confirmed=data[stname]['confirmed'],
                          active=data[stname]['confirmed'],
                          deaths=data[stname]['deaths'],
                          deltaDeaths=data[stname]['deltadeaths'],
                          deltaRecovered= data[stname]['deltarecovered'],
                          deltaConfirmed= data[stname]['deltaconfirmed'],
                          recovered = data[stname]['recovered'],
                          lastupdate = data[stname]['lastupdatedtime'],
                          statecode= data[stname]['statecode']);
            stk.save()

        state_obj = State_k.objects.get(name=stname)
        if('district' in data[stname]):
            state_obj.district_present = True;
            state_obj.save()

            for distName in data[stname]['district']:

                try:
                    dist = District.objects.get(name=distName, state=state_obj)
                    dist.confirmed = data[stname]['district'][distName]['confirmed']
                    dist.deltaConfirmed = data[stname]['district'][distName]['delta']['confirmed']

                    dist.save()
                except Exception as e:
                    dist =District(name=distName,
                                   confirmed = data[stname]['district'][distName]['confirmed'],
                                   deltaConfirmed = data[stname]['district'][distName]['delta']['confirmed'],
                                   state=state_obj)
                    dist.save()

        try:


            param1 = ImpParam.objects.get(key='nongov_totaldeaths')
            param2 = ImpParam.objects.get(key='nongov_totalconfirmed')
            param3 = ImpParam.objects.get(key='nongov_totalrecovered')
            param4 = ImpParam.objects.get(key='nongov_active')
            param5 = ImpParam.objects.get(key='nongov_deltadeaths')
            param6 = ImpParam.objects.get(key='nongov_deltaconfirmed')
            param7 = ImpParam.objects.get(key='nongov_deltarecovered')
            param8 = ImpParam.objects.get(key='nongov_lastupdate')



            param1.value = nongov['deaths']
            param2.value = nongov['confirmed']
            param3.value = nongov['recovered']
            param4.value = nongov['active']
            param5.value = nongov['deltadeaths']
            param6.value = nongov['deltaconfirmed']
            param7.value = nongov['deltarecovered']
            param8.value = nongov['lastupdatedtime']


            param1.save()
            param2.save()
            param3.save()
            param4.save()
            param5.save()
            param6.save()
            param7.save()
            param8.save()


        except Exception as e:

            param1 = ImpParam(key='nongov_totaldeaths',value = nongov['deaths'])
            param2 = ImpParam(key='nongov_totalconfirmed',value = nongov['confirmed'])
            param3 = ImpParam(key='nongov_totalrecovered',value = nongov['recovered'])
            param4 = ImpParam(key='nongov_active',value = nongov['active'])
            param5 = ImpParam(key='nongov_deltadeaths',value = nongov['deltadeaths'])
            param6 = ImpParam(key='nongov_deltaconfirmed',value = nongov['deltadeaths'])
            param7 = ImpParam(key='nongov_deltarecovered',value = nongov['deltarecovered'])
            param8 = ImpParam(key='nongov_lastupdate',value = nongov['lastupdatedtime'])


            param1.save()
            param2.save()
            param3.save()
            param4.save()
            param5.save()
            param6.save()
            param7.save()
            param8.save()
def update():
    fetchData()
    findDataSample2()

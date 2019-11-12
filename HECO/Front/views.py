from django.shortcuts import render
from .models import Raw_Data
from datetime import datetime


# Create your views here.
def Home(request):
    name = ['i']
    datas = []
    date = []


    charge_station = Raw_Data.objects.all()
    ticker = 0
    for n in charge_station:
        for y in name:
            if (n.Charge_Station_Name == y):
                ticker = ticker + 1
        if ticker == 0:
            name.append(n.Charge_Station_Name)
            if name[0] == 'i':
                del name[0]
        ticker = 0

    for r in name:
        datas.append(Raw_Data.objects.filter(Charge_Station_Name=r))

    timer = Raw_Data.objects.filter(Charge_Station_Name='A')

    counter = 0

    for f in timer:
        if int(f.Start_Time) > int(counter):
            counter = f.Start_Time

    day = 86400
    mintime = int(counter) - (day * 7)
    mintime = int(mintime)

    for n in timer:
        if n.Start_Time > mintime:
            readtime = datetime.utcfromtimestamp(n.Start_Time).strftime('%Y-%m-%d %H:%M:%S')
            date.append(str(readtime))

    return render(request, 'Homepage.html', {'station': name, 'data': datas, 'time': timer, 'mintime': int(mintime), 'date': date})

def power_Graph(request):
    name = ['i']
    show = []
    Data = []
    Date = []

    start_time = 0
    end_time = 0

    charge_station = Raw_Data.objects.all()
    ticker = 0
    for n in charge_station:
        for y in name:
            if (n.Charge_Station_Name == y):
                ticker = ticker + 1
        if ticker == 0:
            name.append(n.Charge_Station_Name)
            if name[0] == 'i':
                del name[0]
        ticker = 0

    for f in Raw_Data.objects.filter(Charge_Station_Name='A'):
        if int(f.Start_Time) > int(end_time):
            end_time = f.Start_Time

    day = 86400
    start_time = int(end_time) - (day * 7)
    start_time = int(start_time)

    for n in Raw_Data.objects.filter(Charge_Station_Name='A'):
        if n.Start_Time > start_time:
            readtime = datetime.utcfromtimestamp(n.Start_Time).strftime('%Y-%m-%d %H:%M:%S')
            Date.append(str(readtime))

    if request.method == 'POST':
        for p in request.POST:
            if p == 'info':
                for x in request.POST:
                    start_time = (request.POST['start_time'])
                    start_time = datetime.strptime(start_time, "%Y-%m-%d")
                    start_time = int(start_time.timestamp()) - 36000
                    end_time= (request.POST['end_time'])
                    end_time = datetime.strptime(end_time, "%Y-%m-%d")
                    end_time = int(end_time.timestamp()) - 36000
                    for y in name:
                        if x == y:
                            show.append(x)
                            print(x)

    for q in show:
        Data.append(Raw_Data.objects.filter(Charge_Station_Name=q))


    for e in Raw_Data.objects.filter(Charge_Station_Name='A'):
        if int(e.Start_Time) > int(start_time):
            if int(e.Start_Time) < int(end_time):
                readtime = datetime.utcfromtimestamp(e.Start_Time).strftime('%Y-%m-%d %H:%M:%S')
                Date.append(str(readtime))






    return render(request, 'Graph.html', {'station': name, 'show': show, 'data': Data, 'start_time': start_time, 'end_time': end_time, 'Date': Date})
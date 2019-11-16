from django.shortcuts import render
from .models import Raw_Data
from datetime import datetime
from .backend import meters, findDailyPercentage, con, predication


# Create your views here.
def Home(request):
    name = ['i']
    datas = []
    date = []
    errors = []
    realtime = []


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

    print(predication)

    for n in timer:
        if n.Start_Time > mintime:
            date.append(n.Start_Time)

    print (len(date))

    for i in date:
        for f in range(len(date)):
            d = f + 1
            if date[0] > date[1]:
                new = date[d]
                date[d] = date[f]
                date[f] = new

    for t in date:
        readtime = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
        realtime.append(str(readtime))


    for u in meters:
        for d in u.problems:
            errors.append(d.problemDesc)

    return render(request, 'Homepage.html', {'station': name, 'data': datas, 'time': timer, 'mintime': int(mintime), 'date': realtime, 'error': errors, 'prediction': predication, 'checker': date})

def power_Graph(request):
    name = ['i']
    show = []
    Data = []
    Date = []
    realtime = []

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

    if request.method == 'POST':
        for p in request.POST:
            if p == 'info':
                Date = []
                for x in request.POST:
                    start_time = (request.POST['start_time'])
                    start_time = datetime.strptime(start_time, "%Y-%m-%d")
                    start_time = int(start_time.timestamp()) - 36000
                    end_time = (request.POST['end_time'])
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
                Date.append(e.Start_Time)

    for i in Date:
        for f in range(len(Date)):
            d = f + 1
            if Date[0] > Date[1]:
                new = Date[d]
                Date[d] = Date[f]
                Date[f] = new

    for t in Date:
        readtime = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
        realtime.append(str(readtime))




    return render(request, 'Graph.html', {'station': name, 'show': show, 'data': Data, 'start_time': start_time, 'end_time': end_time, 'Date': realtime, 'date': Date})
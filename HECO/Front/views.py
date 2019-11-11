from django.shortcuts import render
from .models import Raw_Data
from .backend import find_problems


# Create your views here.
def Home(request):
    name = ['i']
    datas = []

    find_problems()


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

    print(name)

    return render(request, 'Homepage.html', {'station': name, 'data': datas, 'time': timer, 'mintime': int(mintime)})
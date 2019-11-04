from django.shortcuts import render
from django.http import HttpResponse
from .models import Raw_Data
# Create your views here.
def Home(request):
    name = ['i']
    charge_station = Raw_Data.objects.all()
    ticker = 0
    for n in charge_station:
        for y in name:
            if (n.Charge_Station_Name == y):
                ticker = ticker + 1
                print(ticker, n.Charge_Station_Name)

        if ticker == 0:
            print(name)
            name.append(n.Charge_Station_Name)

            if name[0] == 'i':
                del name[0]
        ticker = 0


    print(name)

    return render(request, 'Homepage.html', {'station': name})
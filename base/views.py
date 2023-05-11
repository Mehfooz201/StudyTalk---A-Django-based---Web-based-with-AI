from django.shortcuts import render, HttpResponse
from .models import Room



# Create your views here.
def home(request):
    room = Room.objects.all()
    context = {'room':room}
    return render(request, 'base/home.html', context)

def rooms(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room':room}
    return render(request, 'base/room.html', context)

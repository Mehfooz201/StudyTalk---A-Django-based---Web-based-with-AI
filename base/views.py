from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm



# Create your views here.
def home(request):
    #Search Filtering
    q = request.GET.get('q') if request.GET.get('q') != None else 'S'
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    topics = Topic.objects.all()
    room_count = room.count()
    context = {'room':room, 
               'topics':topics, 
               'room_count':room_count}
    return render(request, 'base/home.html', context)

def rooms(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room':room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST,  instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})
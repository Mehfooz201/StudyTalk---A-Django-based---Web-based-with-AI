from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user':user,
        'rooms':rooms,
        'room_messages': room_messages,
        'topics':topics
    }
    return render(request, 'base/profile.html', context)



#Login Page
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doest not exist.")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username & Password doest not exist.")
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

#Logout
def logoutUser(request):
    logout(request)
    return redirect('home')

#Register user
def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration !')
    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html', context)


# Create your views here.
def home(request):
    #Search Filtering
    q = request.GET.get('q') if request.GET.get('q') != None else 'S'
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q) )

    context = {'rooms':rooms, 
               'topics':topics, 
               'room_count':room_count,
               'room_messages':room_messages
               }
    return render(request, 'base/home.html', context)

def rooms(request, pk):
    rooms = Room.objects.get(id=pk)
    room_messages = rooms.message_set.all().order_by('-created')
    participants = rooms.participants.all()


    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            rooms = rooms,
            body = request.POST.get('body')
        )
        rooms.participants.add(request.user)
        return redirect('room', pk=rooms.id)

    context = {'rooms':rooms, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)



@login_required(login_url="/login/")
def createRoom(request):
    form = RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url="/login/")
def updateRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    form = RoomForm(instance=rooms)

    if request.user != rooms.host:
        return HttpResponse('You are not allowed here !')

    if request.method == 'POST':
        form = RoomForm(request.POST,  instance=rooms)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url="/login/")
def deleteRoom(request, pk):
    rooms = Room.objects.get(id=pk)

    if request.user != rooms.host:
        return HttpResponse('You are not allowed here !')
    
    if request.method == 'POST':
        rooms.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':rooms})



# Delete Mesage
@login_required(login_url="/login/")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here !')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})
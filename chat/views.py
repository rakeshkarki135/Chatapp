from django.shortcuts import render,redirect
from .models import Room, Message
from django.http  import HttpResponse,HttpResponseRedirect,JsonResponse

# Create your views here.
def home(request):
     return render(request , 'home.html' )


def room(request , room):
     username=request.GET.get('username')
     room_details=Room.objects.get(name=room)
     return render(request , 'room.html' , { 
                         'username':username,
                         'room':room,
                         'room_details':room_details,
                                            })

def checkview(request):
     room=request.POST['room_name']
     username = request.POST['username']
     
     if Room.objects.filter(name=room).exists():
          return redirect('/'+room +'/?username='+username)
     else:
          new_room=Room.objects.create(name=room)
          new_room.save()
          return redirect('/'+room +'/?username='+username)
     
     
def send(request):
     message=request.POST.get('message')
     username=request.POST.get('username')
     room_id=request.POST.get('room_id')
     
     try:
        new_message=Message.objects.create(value=message , user=username, room=room_id)
        new_message.save()
        return HttpResponse('Message Sent Successfully')
     
     except:
        pass
     return redirect('room')

def getMessages(request ,room):
     room_details=Room.objects.get(name=room)
     
     # filtering the data using the room_id that we get from  room_details id.
     messages=Message.objects.filter(room__icontains=room_details.id)
     # creating the list of the values from the messages
     return JsonResponse({"messages":list(messages.values())})
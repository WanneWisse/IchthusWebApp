from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, UserQuestionAnswer, UserEvent, Tickie, UserTickieAnswer
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth import logout
from django.shortcuts import redirect
import base64



@login_required(login_url='/login_user')
def index(request):
    #upcoming_events = Event.objects.filter(date__gte=datetime.date.today())
    upcoming_events = Event.objects.order_by('-date')
    user_registered = []
    for e in upcoming_events:
        users = e.users.all()
        #e.users = users
        if request.user in users:
            user_registered.append("ja")
        else:
            user_registered.append("nee")
    events_with_register = zip(upcoming_events,user_registered)
    context = {'events_with_register': events_with_register, "user":request.user}

    return render(request, 'IchthusWebApp/index.html', context)

@login_required(login_url='/login_user')
def event_detail(request,event_id):
    event = Event.objects.filter(id=event_id).all()[0]
    registered = False
    users = event.users.all()
    if request.user in users:
        registered = True

    questions = event.question_set.all()
    q_with_a = {}
    for q in questions:
        question = str(q.text)
        q_with_a[question] = []
        answers = UserQuestionAnswer.objects.filter(question=q).select_related('userevent').all()
        for a in answers:
            user = a.userevent.user
            q_with_a[question].append((a.answer,user))
    
    tickies = event.tickie_set.all()
    t_with_a = {}
    for t in tickies:
        tickie = str(t.name)
        t_with_a[tickie] = {}
        t_with_a[tickie]["id"] = t.id
        t_with_a[tickie]["image"] = t.image
        t_with_a[tickie]["url"] = t.url
        t_with_a[tickie]["user_paid"] = False
        t_with_a[tickie]["users"] = []
        paid_users = UserTickieAnswer.objects.filter(tickie=t).select_related('userevent').all()
        for p in paid_users:
            user = p.userevent.user
            t_with_a[tickie]["users"].append(user)
            if request.user == user:
                t_with_a[tickie]["user_paid"] = True
    context = {"event": event, "registered": registered, 'tickies_with_answers': t_with_a.items(),  'questions':questions, 'questions_with_answers': q_with_a.items()}
    return render(request, 'IchthusWebApp/event_detail.html', context)

@login_required(login_url='/login_user')
def image_post(request):
    if request.method =='POST':
        event_id = request.POST['id']
        event = Event.objects.filter(id=event_id).all()[0]
        name = request.POST['name']
        url = request.POST['url']
        image = request.FILES['file']
        base_string = str(base64.b64encode(image.file.read()),"utf-8")
        content_type = image.content_type
        new_tickie = Tickie(name=name,url=url,image_type=content_type,image=base_string,event=event)
        new_tickie.save()
        return event_detail(request=request,event_id=event_id)

def register_user(request):
    if request.method =='POST':
        username_input = request.POST['username']
        password = request.POST['password']
        extra_pass = request.POST['extra_password']
        error = None
        if extra_pass!= "extra":
            error = "password not correct"
        
        elif User.objects.filter(username = username_input).all():
            error = "user already exists"
        else:
            user = User.objects.create_user(username_input, 'i@gmail.com', password)
            if user != None:
                user = authenticate(username=username_input, password=password)
                return index(request)
        context = {"error":error}
        return render(request, 'IchthusWebApp/register_user.html', context)
    else:
        return render(request, 'IchthusWebApp/register_user.html')

def login_user(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            context = {"error":"wrong username/password"}
            return render(request, 'IchthusWebApp/login_user.html', context)
    else:
        return render(request, 'IchthusWebApp/login_user.html')

@login_required(login_url='/login_user')
def logout_user(request):
    logout(request)
    return redirect(login_user)

@login_required(login_url='/login_user')
def register_user_event(request):
    if request.method == 'POST':
        event_id = request.POST['id']
        event = Event.objects.filter(id=event_id).all()[0]
        event.users.add(request.user)
        event_questions = event.question_set.all()
        userevent = UserEvent.objects.filter(event=event).filter(user=request.user).all()[0]
        for event_question in event_questions:
            question_id = event_question.id
            question_answer = request.POST['question' + str(question_id)]
            uqa = UserQuestionAnswer(userevent=userevent,question=event_question,answer=question_answer)
            uqa.save()
    return redirect(index)

@login_required(login_url='/login_user')
def deregister_user_event(request):
    if request.method == 'POST':
        event_id = request.POST['id']
        event = Event.objects.filter(id=event_id).all()[0]
        event.users.remove(request.user)
        return redirect(index)

@login_required(login_url='/login_user')
def change_paid(request, tickie_id):
    tickie = Tickie.objects.filter(id=tickie_id).all()[0]
    user_event = UserEvent.objects.filter(user=request.user).filter(event=tickie.event).all()[0]
    userticketanswer = UserTickieAnswer.objects.filter(tickie=tickie).filter(userevent=user_event).all()
    if not userticketanswer:
        user_tickie_answer = UserTickieAnswer(tickie=tickie,userevent=user_event)
        user_tickie_answer.save()
    else:
        userticketanswer[0].delete()
    return event_detail(request=request,event_id=user_event.event.id)




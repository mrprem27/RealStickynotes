from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import date
# from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict
from .models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    if not request.session.get('user'):
        return render(request, "todo/index.html", {"user_status": "neg"})
    user_acc = User.objects.get(pk=int(request.session['user']))
    return render(request, "todo/index.html", {"user_status": "pos", "tasks": user_acc.task_ls.all()})


def add_task(request):
    if(request.method == "POST"):
        form = request.POST
        title = form.get('title')
        description = form.get('description')
        uploaded_file = request.FILES.get('img')
        # if not uploaded_file:
        #     uploaded_file=
        priority = form.get('priority')
        # user_id = form.get('user_id')
        user_id = request.session['user']
        new_task = Task(title=title, description=description,
                        status=False, user=User.objects.get(pk=int(user_id)), priority=priority)
        if uploaded_file:
            new_task.img = uploaded_file
        new_task.save()
        new_task_json = model_to_dict(new_task)
        new_task_json["date"] = date.today()
        new_task_json['img'] = new_task.img.url
    return JsonResponse({"status": "success", "new_task": new_task_json})
# [{"model": "todo.task", "pk": 7, "fields": {"title": "dasdcca", "description": "ascascasc", "date": "2021-08-03", "img": "uploads/images/wallpaper2you_341572.jpg", "status": false, "user": 1, "priority": "6"}}]


@csrf_exempt
def mark_task(request):
    if(request.method == "POST"):
        fval = eval(request.POST.get('json_val'))
        if fval['mark'] == "True":
            Task.objects.filter(pk=int(fval['id'])).update(status=False)
        else:
            Task.objects.filter(pk=int(fval['id'])).update(status=True)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"})


@csrf_exempt
def del_task(request):
    if(request.method == "POST"):
        fval = eval(request.POST.get('json_val'))
        Task.objects.get(pk=int(fval['id'])).delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"})


@csrf_exempt
def open(request):
    if(request.method == "POST"):
        if(request.method == "POST"):
            fval = eval(request.POST.get('json_val'))
            new_task = Task.objects.get(pk=int(fval['id']))
            new_task_json = model_to_dict(new_task)
            new_task_json['img'] = new_task.img.url
        return JsonResponse({"status": "success", "new_task": new_task_json})


def search_task(request):
    if(request.method == "POST"):
        form = request.POST
        string = form.get('task_search')
        fsend = []
        if string == "*":
            user_acc = User.objects.get(pk=int(request.session['user']))
            send = list(user_acc.task_ls.all())
        else:
            user_acc = User.objects.get(pk=int(request.session['user']))
            send = list(user_acc.task_ls.filter(title__contains=string))
        for ss in send:
            temp = model_to_dict(ss)
            temp["date"] = ss.date
            temp['img'] = ss.img.url
            fsend.append(temp)
    return JsonResponse({"status": "success", "new_task": fsend})


def add_user(request):
    if(request.method == "POST"):
        form = request.POST
        name = form.get('name')
        email = form.get('email_register')
        password = form.get('pass_register')
        l = User.objects.filter(email=email)
        if len(l):
            return JsonResponse({"status": "fail"})
        new_user = User(name=name, password=make_password(
            password), email=email)
        new_user.save()
        return JsonResponse({"status": "success"})


def login(request):
    if(request.method == "POST"):
        form = request.POST
        email = form.get('email')
        cc = User.objects.filter(email=email)
        if len(cc) == 0:
            return JsonResponse({"status": "fail"})
        user_acc = cc.first()
        password = form.get('password')
        if check_password(password, user_acc.password):
            request.session['user'] = user_acc.id
            fsend = []
            send = list(user_acc.task_ls.all())
            for ss in send:
                temp = model_to_dict(ss)
                temp["date"] = ss.date
                temp['img'] = ss.img.url
                fsend.append(temp)
            return JsonResponse({"status": "success", "task": fsend})
        else:
            return JsonResponse({"status": "fail"})


def logout(request):
    request.session.clear()
    return JsonResponse({"status": "success"})


def edit(request):
    if(request.method == "POST"):
        form = request.POST
        taskid = form.get('taskid')
        print(taskid)
        uploaded_file = request.FILES.get('img')
        Task.objects.filter(pk=int(taskid)).update(title=form.get(
            'title'), description=form.get('description'), priority=form.get('priority'))
        tsk=Task.objects.get(pk=int(taskid))
        new_task_json = model_to_dict(tsk)
        new_task_json["date"] = tsk.date
        new_task_json['img'] = tsk.img.url
    return JsonResponse({"status": "success", "new": new_task_json})

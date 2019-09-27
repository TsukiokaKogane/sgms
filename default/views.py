from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import StudentInfo, TeacherInfo, CourseInfo, ClassInfo,StudentCourse
from django.contrib.auth import authenticate,login,logout
import django.utils.timezone as timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

import math
# Create your views here.

# @login_required
# def testView(request):
#     return render(request, 'test.html')


def loginview(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('')
    return render(request, 'login.html')

@login_required
def manageview(request):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('')
    studentlist = StudentInfo.objects.all()
    teacherlist = TeacherInfo.objects.all()
    courselist = CourseInfo.objects.all()
    classlist = ClassInfo.objects.all()
    return render(request, 'manage.html', {'username': request.session['username'],
                                           'studentlist': studentlist,
                                           'teacherlist': teacherlist,
                                           'courselist': courselist,
                                           'classlist': classlist,
                                           })


@login_required
def autoredirect(request):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect('/login')
    if request.session['mask'] == 0:
        return HttpResponseRedirect('/manage')
    if request.session['mask'] == 1:
        return HttpResponseRedirect('/dashboard')
    if request.session['mask'] == 2:
        return HttpResponseRedirect('/gradelist')

@login_required
def newstuview(request, msg=''):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('')
    return render(request, 'newstu.html', {'username': request.session['username'],'msg':msg})


@login_required
@csrf_exempt
def newstudef(request):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('')
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    name = request.POST.get('name')
    cls = request.POST.get('cls')
    if User.objects.filter(username=username):
        msg = 'username has been taken.'
        return newstuview(request, msg)
    p = User.objects.create_user(username=username, password=password, first_name = name,last_name='student')
    q = StudentInfo(user=p, cls=cls)
    q.save()
    r = ClassInfo.objects.filter(cls=cls)
    for i in r:
        if StudentCourse.objects.filter(course=i.course,stu=p).exists() == False:
            s = StudentCourse(course=i.course, stu=p, pt=0)
            s.save()
    return HttpResponseRedirect('/')


@login_required
def newteaview(request, msg=''):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('')
    return render(request, 'newteacher.html', {'username': request.session['username'], 'msg':msg})


@login_required
@csrf_exempt
def newteadef(request):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    name = request.POST.get('name')
    if User.objects.filter(username=username):
        msg = 'username has been taken.'
        return newteaview(request, msg)
    p = User.objects.create_user(username=username, password=password, first_name=name, last_name='teacher')
    q = TeacherInfo(user=p)
    q.save()
    return HttpResponseRedirect('/')

@login_required
def newcorview(request, msg=''):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    return render(request, 'newcourse.html', {'username': request.session['username'], 'msg': msg})


@login_required
@csrf_exempt
def newcordef(request):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    name = request.POST.get('name')
    ID = request.POST.get('id')
    cls = request.POST.get('cls')
    print(name)
    print(ID)
    print(cls)
    if TeacherInfo.objects.filter(user_id=ID).exists() == False:
        msg = 'teacher doesn\'t exist.'
        return newcorview(request, msg)
    if CourseInfo.objects.filter(teacher=User.objects.filter(id=ID)[0],course=name).exists() == True:
        msg = 'this course is already in the system.'
        return newcorview(request, msg)
    p = CourseInfo(teacher=User.objects.filter(id=ID)[0], course=name)
    p.save()
    return HttpResponseRedirect('/')

@login_required
def newclsview(request, msg=''):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    return render(request, 'newclass.html', {'username': request.session['username'], 'msg': msg})


@login_required
@csrf_exempt
def newclsdef(request):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    name = request.POST.get('name')
    ID = request.POST.get('id')
    cls = request.POST.get('cls')
    # print(name)
    # print(ID)
    # print(cls)
    if TeacherInfo.objects.filter(user_id=ID).exists() == False:
        msg = 'teacher doesn\'t exist.'
        return newclsview(request, msg)

    if CourseInfo.objects.filter(teacher=User.objects.filter(id=ID)[0],course=name).exists() == False:
        msg = 'course doesn\'t exist.'
        return newclsview(request, msg)
    course = CourseInfo.objects.filter(teacher=User.objects.filter(id=ID)[0], course=name)[0]
    if ClassInfo.objects.filter(course=course, cls=cls):
        msg = 'this class already has the course in the system.'
        return newclsview(request, msg)
    p = ClassInfo(course=course, cls=cls)
    p.save()
    q = StudentInfo.objects.filter(cls=cls)
    for i in q:
        # print(i.user.first_name)
        # print(course.course)
        if StudentCourse.objects.filter(course=course, stu=i.user).exists() == False:
            r = StudentCourse(course=course, stu=i.user, pt=0)
            r.save()
    return HttpResponseRedirect('/')

@csrf_exempt
def logindef(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    # print(username)
    # print(password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['username'] = username
            request.session['id'] = user.id
            if user.is_superuser == 1:
                request.session['mask'] = 0 #admin
            else:
                if user.last_name == 'student':
                    request.session['mask'] = 1 #student
                else:
                    request.session['mask'] = 2 #teacher
            # print('why')
            return autoredirect(request)

    return render(request, 'login.html')


@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required
def deldef(request, ID):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    User.objects.filter(id=ID).delete()
    return HttpResponseRedirect('/')

@login_required
def delcdef(request, course,ID):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    CourseInfo.objects.filter(teacher=User.objects.filter(id=ID)[0], course=course).delete()
    return HttpResponseRedirect('/')


@login_required
def delcldef(request, ID):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    ClassInfo.objects.filter(id=ID).delete()
    return HttpResponseRedirect('/')

@login_required
def editsview(request, ID):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    p = StudentInfo.objects.filter(user_id=ID)[0]
    return render(request, 'editstu.html',{
        'username': p.user.username,
        'Username': request.session['username'],
        'name': p.user.first_name,
        'ID': ID,
        'cls': p.cls
    })


@login_required
@csrf_exempt
def editsdef(request):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    # print('fucked')
    ID = request.POST.get('ID')
    cls = request.POST.get('cls')
    p = StudentInfo.objects.get(user_id=ID)
    if p.cls != cls:
        r = ClassInfo.objects.filter(cls=cls)
        for i in r:
            if StudentCourse.objects.filter(course=i.course, stu = p.user).exists() == False:
                s = StudentCourse(course=i.course, stu=p.user, pt=0)
                s.save()
        p.cls = cls
        p.save()
    # print(ID)
    # print(cls)
    return HttpResponseRedirect('/')


@login_required
def dashview(request):
    if request.session['mask'] != 1:
        return HttpResponseRedirect('/')
    stu = User.objects.get(id=request.session['id'])
    gradelist = StudentCourse.objects.filter(stu=stu)
    return render(request, 'dashboard.html',{
        'username': request.session['username'],
        'gradelist': gradelist,
    })


@login_required
def proview(request):
    if request.session['mask'] != 1:
        return HttpResponseRedirect('/')
    p = StudentInfo.objects.get(user_id=request.session['id'])
    return render(request, 'profile.html',{
        'name': p.user.first_name,
        'ID': p.user_id,
        'cls': p.cls,
    })


@login_required
def graview(request):
    if request.session['mask'] != 2:
        return HttpResponseRedirect('/')
    p = User.objects.get(id=request.session['id'])
    courselist = CourseInfo.objects.filter(teacher=p)
    gradelist = StudentCourse.objects.all()
    return render(request, 'gradelist.html', {
        'username': request.session['username'],
        'courselist': courselist,
        'gradelist': gradelist,
    })

@login_required
def tproview(request):
    if request.session['mask'] != 2:
        return HttpResponseRedirect('/')
    # p = StudentInfo.objects.get(user_id=request.session['id'])
    p = TeacherInfo.objects.get(user_id=request.session['id'])
    return render(request, 'tprofile.html',{
        'name': p.user.first_name,
        'ID': p.user_id,
    })

@login_required
def editgdef(request,cid,sid):
    if request.session['mask'] != 2:
        return HttpResponseRedirect('/')

    p = StudentCourse.objects.get(stu=User.objects.get(id=sid), course=CourseInfo.objects.get(id=cid))
    # print(p.pt)
    # print(p.id)
    return render(request,'editgrade.html',{
       'username': request.session['username'],
        'name': p.stu.first_name,
        'ID': p.stu.id,
        'course': p.course.course,
        'scid':p.id,
        'pt': p.pt,
    }
    )

@login_required
@csrf_exempt
def editgsub(request):
    if request.session['mask'] != 2:
        return HttpResponseRedirect('/')
    scid = request.POST.get('scid')
    pt = request.POST.get('pt')
    p = StudentCourse.objects.get(id=scid)
    p.pt = pt
    p.save()
    # print(scid)
    # print(pt)
    return HttpResponseRedirect('/')

def chartview(request):
    if request.session['mask'] != 0:
        return HttpResponseRedirect('/')
    courselist = CourseInfo.objects.all()
    datalist = []
    namelist = []
    for course in courselist:
        gradelist = StudentCourse.objects.filter(course=course)

        # print('!')
        templist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        namelist.append(course.course)
        for grade in gradelist:
            # print(grade.pt)
            for i in range(1, 11):
                if i*10.0 >= grade.pt:
                    templist[i-1] += 1
                    break
        # print(templist)
        datalist.append(templist)
    # print(namelist)
    # print(datalist)
    stulist = StudentInfo.objects.all()
    pielist = []
    clslist = []
    hasht =[]
    for stu in stulist:
        if stu.cls in hasht:
            continue
        hasht.append(stu.cls)
        clslist.append(stu.cls)
        print(stu.cls)
        print(StudentInfo.objects.filter(cls=stu.cls).count())
        pielist.append(StudentInfo.objects.filter(cls=stu.cls).count())

    # data = [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1]
    return render(request, 'chart.html', {
        'username': request.session['username'],
         'namelist': namelist,
        'datalist': datalist,
        'pielist': pielist,
        'classlist': clslist,
    }
                  )

def resetpview(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, 'reset.html')

def resetpdef(request):
    # print('y?')
    if request.user.is_authenticated:
        # print('no')
        return HttpResponseRedirect('/')
    username = request.POST.get('username')
    password = request.POST.get('password')
    # print(username)
    # print(password)
    if User.objects.filter(username = username).exists() == True:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return HttpResponseRedirect('/login')
    return render(request, 'reset.html',{'msg':'this user doesnt exist.' })
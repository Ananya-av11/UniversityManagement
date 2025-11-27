from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import Teacher,Course,Student
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
import os,re
from urllib.parse import urlencode
from django.urls import reverse

# Create your views here.
def loginpage(request):
    return render(request,'loginpage.html')
def signup(request):
    coursetb=Course.objects.all()
    return render(request,'signup.html',{'course':coursetb})
def teacher_add(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        address=request.POST['address']
        age=request.POST['age']
        email=request.POST['email']
        phone=request.POST['phone']
        if not re.match(r'^\d{10}$',phone):
            messages.info(request,'Invalid phone number. It must be 10 digits long.')
            return redirect('signup')
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        uimg=request.FILES.get('img')
        tcourse=request.POST['tcourse']
        cn=Course.objects.get(id=tcourse)
        if password==cpassword:
            if User.objects.filter(username=uname).exists():
                messages.info(request,'This username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=password)
                user.save()
                usr=User.objects.get(id=user.id)
                teach=Teacher(age=age,address=address,phone=phone,image=uimg,course=cn,user=usr)
                teach.save()
                messages.info(request,'Successfully Inserted Teacher Details')
                return redirect('signup')
        else:
            messages.info(request,'Password does not match')
            return redirect('signup')

def loginfun(request):
    if request.method == 'POST':
        username=request.POST['uname']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_authenticated:  # Check if the user is authenticated
                if user.is_staff:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    return redirect('adminhome')
                else:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    messages.info(request, f'Welcome {user}')
                    return redirect('teacherhome')  # Redirect to techhome after login   
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('loginpage')
    return render(request, 'signup.html')

@login_required(login_url='loginpage')
def adminhome(request):
    return render(request,'adminhome.html')

def addcourse(request):
    return render(request,'addcourse.html')
def course_add(request):
    if request.method == 'POST':
        name=request.POST['cname']
        fee=request.POST['fee']
        cou=Course(coursename=name,fees=fee)
        cou.save()
        messages.info(request,'Course Added Successfully ')
        return redirect('addcourse')
def addstudent(request):
    coursetb=Course.objects.all()
    return render(request,'addstudent.html',{'coursetb':coursetb})
def student_add(request):
    if request.method=='POST':
        stname=request.POST['sname']
        staddress=request.POST['saddress']
        stage=request.POST['sage']
        stdate=request.POST['sdate']
        stcourse=request.POST['scourse']
        cn=Course.objects.get(id=stcourse)
        stud=Student(studentname=stname,address=staddress,age=stage,joiningdate=stdate,course=cn)
        stud.save()
        messages.info(request,'Student Details Added Successfully')
        return redirect('addstudent')
def studentdetails(request):
    stud=Student.objects.all()
    return render(request,'studentdetails.html',{'st':stud})
def updatestudent(request,pk):
    stud=Student.objects.get(id=pk)
    cn=Course.objects.all()
    return render(request,'updatestudent.html',{'st': stud, 'course': cn})


def edit_student(request,pk):
    if request.method == 'POST':
        stud=Student.objects.get(id=pk)
        stud.studentname=request.POST['sname']
        stud.age=request.POST['sage']
        stud.address=request.POST['saddress']
        stud.joiningdate=request.POST['sdate']
        cname=request.POST['scourse']
        cc=Course.objects.get(id=cname)
        stud.course=cc
        stud.save()
        # messages.info(request,'Student Details Updated Successfully')
        return redirect('studentdetails')
def deletestudent(request,pk):
    stud=Student.objects.get(id=pk)
    stud.delete()
    return redirect('studentdetails')
    
def teacherview(request):
    teach=Teacher.objects.all()
    return render(request,'teacherdetails.html',{'te':teach})
def deleteteacher(request,pk):
    teach=Teacher.objects.get(id=pk)
    usr=teach.user
    teach.delete()
    usr.delete()
    return redirect('teacherview')

# def teacherdetails(request):
#     return render(request,'teacherdetails.html')
@login_required(login_url='loginpage')
def teacherhome(request):
    if 'user' in request.session:
        return render(request,'teacherhome.html')
    else:
        query_params = {'error': 'access_denied'}
        url = '{}?{}'.format(reverse('homepage'), urlencode(query_params))
        return redirect(url)

# def teachercard(request):
#     return render(request,'teachercard.html')
    
# def teachercard(request):
#         tchr=Teacher.objects.get(user=request.user)
#         cr=Course.objects.all()
#         return render(request,'teachercard.html',{'tcr':tchr,'csr':cr})
def teachercard(request):
    tchr = Teacher.objects.filter(user=request.user).first()  # Prevents "DoesNotExist" error
    return render(request, 'teachercard.html', {'tcr': tchr})

def updateteacher(request):
    
    tch=Teacher.objects.get(user=request.user)
    crcs=Course.objects.all()
    return render(request,'updateteacher.html',{'tchr':tch, 'crse':crcs})
def edit_teacher(request):
    if request.method == 'POST':
        teach=Teacher.objects.get(user=request.user)
        user=request.user
        user.first_name=request.POST['fname']
        user.last_name=request.POST['lname']
        uname=request.POST['uname']
        if User.objects.filter(username=uname).exclude(pk=user.pk).exists():
                messages.info(request,'This username already exists')
                return redirect('updateteacher')
        
        user.username=uname
        user.email=request.POST['email']
        
        phone=request.POST['phone']
        if not re.match(r'^\d{10}$',phone):
            messages.info(request,'Invalid phone number. It must be 10 digits long.')
            return redirect('updateteacher')
        user.save()
        
        teach.address=request.POST['address']
        teach.age=request.POST['age']
        teach.phone=phone
        
        timg=request.FILES.get('img')
        if timg:
            if teach.image:
                os.remove(teach.image.path)
            teach.image=timg
        cname=request.POST['tcourse']
        cc=Course.objects.get(id=cname)
        teach.course=cc
        teach.save()
        # messages.info(request,'Teacher Details Updated Successfully')
        return redirect('teachercard')
    return render(request,'teacherhome.html')

def logoutfun(request):
    auth.logout(request)
    return redirect('loginpage')
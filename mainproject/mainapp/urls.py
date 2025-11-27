from django.urls import path
from .import views

urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('signup',views.signup,name='signup'),
    path('loginfun',views.loginfun,name='loginfun'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('addcourse',views.addcourse,name='addcourse'),
    path('course_add',views.course_add,name='course_add'),
    path('addstudent',views.addstudent,name='addstudent'),
    path('student_add',views.student_add,name='student_add'),
    path('studentdetails',views.studentdetails,name='studentdetails'),
    path('updatestudent/<int:pk>',views.updatestudent,name='updatestudent'),
    path('edit_student/<int:pk>',views.edit_student,name='edit_student'),
    path('deletestudent/<int:pk>',views.deletestudent,name='deletestudent'),
    path('deleteteacher/<int:pk>',views.deleteteacher,name='deleteteacher'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('teacherview',views.teacherview,name='teacherview'),
    path('teachercard',views.teachercard,name='teachercard'),
    path('updateteacher',views.updateteacher,name='updateteacher'),
    path('edit_teacher',views.edit_teacher,name='edit_teacher'),
    path('teacher_add',views.teacher_add,name='teacher_add'),
    path('logoutfun',views.logoutfun,name='logoutfun')
]
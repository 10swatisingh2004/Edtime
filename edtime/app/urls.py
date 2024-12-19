from django.urls import path
from . import views

urlpatterns = [
    path('',views.landingpage , name='edtime'),
   
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('appointments/', views.view_appointments, name='view_appointments'),
    path('send_message/<int:appointment_id>/', views.send_message, name='send_message'),
    path('book_appointment/<int:teacher_id>/', views.book_appointment, name='book_appointment'),


    # Teacher views
    path('teachers/', views.teachers, name='teachers'),
    path('book_appointment/<int:teacher_id>/', views.book_appointment, name='book_appointment'),
    
    # Admin views
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('update_teacher/<int:teacher_id>/', views.update_teacher, name='update_teacher'),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('approve_student/<int:student_id>/<str:action>/', views.approve_student, name='approve_student'),
    path('approve_cancel_appointment/<int:appointment_id>/<str:action>/', views.approve_cancel_appointment, name='approve_cancel_appointment'),
]

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Teacher, Appointment, Message, Student
from django.contrib.auth.decorators import login_required, user_passes_test
 

def landingpage(request):
    return render(request,'index.html')
# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

# Admin Dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    teachers = Teacher.objects.all()
    students = Student.objects.filter(is_approved=False)  # Unapproved students
    return render(request, 'admin/admin_dashboard.html', {'teachers': teachers, 'students': students})
# View for students to book an appointment with a teacher
@login_required
def book_appointment(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    if request.method == "POST":
        date = request.POST['date']
        message = request.POST['message']
        Appointment.objects.create(
            student=request.user,
            teacher=teacher,
            date=date,
            message=message,
        )
        messages.success(request, "Appointment booked successfully!")
        return redirect('teachers')
    return render(request, 'student/book_appointment.html', {'teacher': teacher})

# Add Teacher (Admin)
import logging
logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_admin)
def add_teacher(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        department = request.POST['department']
        subject = request.POST['subject']

        logger.info(f"Received form data: {username}, {department}, {subject}")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            logger.warning("Username already exists.")
            return redirect('add_teacher')

        try:
            user = User.objects.create_user(username=username, password=password)
            Teacher.objects.create(user=user, department=department, subject=subject)
            messages.success(request, "Teacher added successfully!")
            logger.info(f"Teacher {username} added successfully.")
            return redirect('admin_dashboard')
        except Exception as e:
            logger.error(f"Error while adding teacher: {e}")
            messages.error(request, "An error occurred while adding the teacher.")
            return redirect('add_teacher')

    return render(request, 'admin/add_teacher.html')


# Update Teacher (Admin)
@login_required
@user_passes_test(is_admin)
def update_teacher(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    if request.method == "POST":
        teacher.department = request.POST['department']
        teacher.subject = request.POST['subject']
        teacher.save()
        messages.success(request, "Teacher updated successfully!")
        return redirect('admin_dashboard')
    return render(request, 'admin/update_teacher.html', {'teacher': teacher})

# Delete Teacher (Admin)
@login_required
@user_passes_test(is_admin)
def delete_teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.delete()  # This will also delete the related User due to on_delete=models.CASCADE
        messages.success(request, "Teacher and associated user account deleted successfully.")
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher does not exist.")
    return redirect('admin_dashboard')


# Approve or Reject Student Registration (Admin)
@login_required
@user_passes_test(is_admin)
def approve_student(request, student_id, action):
    student = Student.objects.get(id=student_id)
    if action == "approve":
        student.is_approved = True
    elif action == "reject":
        student.delete()
    student.save()
    messages.success(request, "Student registration updated!")
    return redirect('admin_dashboard')

# View All Appointments (Teacher)
@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(teacher__user=request.user)
    return render(request, 'teacher/view_appointments.html', {'appointments': appointments})

# Approve/Cancel Appointment (Teacher)
@login_required
def approve_cancel_appointment(request, appointment_id, action):
    appointment = Appointment.objects.get(id=appointment_id)
    if action == "approve":
        appointment.status = "Approved"
    elif action == "cancel":
        appointment.status = "Canceled"
    appointment.save()
    messages.success(request, "Appointment updated!")
    return redirect('view_appointments')
# View to display a list of teachers (accessible by students)
@login_required
def teachers(request):
    teachers_list = Teacher.objects.all()
    return render(request, 'student/teachers.html', {'teachers': teachers_list})

# Send Message (Student)
@login_required
def send_message(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == "POST":
        content = request.POST['message']
        Message.objects.create(appointment=appointment, sender=request.user, content=content)
        messages.success(request, "Message sent successfully!")
        return redirect('view_appointments')
    return render(request, 'teacher/send_message.html', {'appointment': appointment})

# Register and Login (Student)
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        Student.objects.create(user=user)
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            # Check if the user is an admin
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            
            # Check if the user is a teacher
            try:
                teacher = Teacher.objects.get(user=user)
                return redirect('view_appointments')  # Redirect to teachers page
            except Teacher.DoesNotExist:
                pass
            
            # Check if the user is a student
            try:
                student = Student.objects.get(user=user)
                if student.is_approved:
                    return redirect('teachers')  # Redirect to student appointments
                else:
                    messages.warning(request, "Your account is not approved yet.")
                    return redirect('login')  # Redirect to login if student is not approved
            except Student.DoesNotExist:
                pass

            messages.error(request, "User not found.")
            return redirect('login')
        
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
   
    return render(request, 'login.html')

# Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


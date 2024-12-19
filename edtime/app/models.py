from django.db import models
from django.contrib.auth.models import User

# Model for Teachers (Inherits from User)
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Deletes user when teacher is deleted
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# Model for Appointments
class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField()
    message = models.TextField()
    status = models.CharField(max_length=20, default="Pending")  # Pending, Approved, Canceled

    def __str__(self):
        return f"{self.student.username} - {self.teacher.user.username} on {self.date}"

# Model for Messages
class Message(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

# Model for Students (Admin can approve or reject registration)
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

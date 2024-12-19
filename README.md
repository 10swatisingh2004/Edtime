# Student-Teacher Appointment Booking System

This is a web application built with Django that enables students to book appointments with teachers and allows admins to manage teachers, students, and appointments. The system is designed with three types of users:
1. **Admin**: Can manage teachers, students, and appointments.
2. **Teacher**: Can view and approve or cancel appointments.
3. **Student**: Can book appointments with teachers, view teachers, and send messages.

## Features

- **Student Features**:
  - Register and log in to the platform.
  - View a list of available teachers.
  - Book appointments with teachers.
  - View upcoming appointments and send messages to teachers.

- **Teacher Features**:
  - View appointments scheduled with them.
  - Approve or cancel appointments.
  - Send messages to students regarding appointments.

- **Admin Features**:
  - Manage teachers (add, update, delete).
  - Approve or reject student registrations.
  - View and manage all appointments.

## Project Setup

Follow these steps to set up the project locally:

### 1. Clone the repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/10swatisingh2004/Edtime.git
cd edtime
```
 ### 2. Install Dependencies
Ensure you have Python and Django installed. Then install the required dependencies using:

```bash
pip install -r requirements.txt
```
### 3. Set Up the Database
Run the migrations to set up the database:

```bash
python manage.py migrate
```

### 4. Create a Superuser (Admin Account)
To access the admin dashboard, create a superuser by running:

```bash
python manage.py createsuperuser
```
Follow the prompts to set the username, email, and password.

### 5.Run the Development Server
Start the development server:

```bash
python manage.py runserver
```
### 6. Access the Application :
- **Admin Dashboard** : Visit http://localhost:8000/admin and log in with the superuser account.
- **Student Features** : Students can register at http://localhost:8000/register and log in at http://localhost:8000/login.
- **Teacher Features** : Teachers will be able to view and manage their appointments after logging in.

### Running Tests
To run the test suite, execute the following command:
```bash
python manage.py test
```
### Contributing
We welcome contributions to improve this project. Here's how you can contribute:

**Fork the repository.**:
1. Create a new branch (git checkout -b feature-branch).
2. Commit your changes (git commit -m 'Add feature').
3. Push to the branch (git push origin feature-branch).
4. Open a pull request to the main repository.

### License
This project is licensed under the MIT License.

### Author
- Swati Singh - **Developer**.
  

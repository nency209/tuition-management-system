from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import date
from reportlab.lib.pagesizes import letter # type: ignore

             
# Create your views here.
def home(request):
    return render(request,'index.html')

# ------------student inquity to send email with payment---------
def Inquiry(request):
    clas = Class.objects.all()
    states = State.objects.all()
    cities = []
    areas = []

    selected_state = request.GET.get('state_id') or request.POST.get('state_id')
    selected_city = request.GET.get('city_id') or request.POST.get('city_id')

    if selected_state:
        cities = City.objects.filter(state_id=selected_state)

    if selected_city:
        areas = Area.objects.filter(city_id=selected_city)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mob = request.POST.get('no')
        pmob = request.POST.get('pno')
        gender = request.POST.get('gender')
        add = request.POST.get('add')
        pas = request.POST.get('pas')
        bod = request.POST.get('bod')
        class_id = request.POST.get('class_id')
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id')
        area_id = request.POST.get('area_id')
        code = request.POST.get('code')
        image = request.FILES.get('image')
        print(image)
        # Check if email already exists
        alregi = inquiry.objects.filter(email=email)
        if alregi:
            return render(request, 'Admission.html', {
                'al': 'Already registered',
                'cls': clas,
                'states': states,
                'cities': cities,
                'areas': areas,
                'selected_state': selected_state,
                'selected_city': selected_city
            })

        # Check if passwords match
        if pas == request.POST.get('cpas'):
            if class_id and name and email and mob and pmob and city_id and state_id and area_id and code and bod and image:
                print(image)
                class_instance = Class.objects.get(id=class_id)
                state_instance = State.objects.get(id=state_id)
                city_instance = City.objects.get(id=city_id)
                area_instance = Area.objects.get(id=area_id)

                # Create Inquiry Record
                inquiry.objects.create(
                    name=name, email=email, mob=mob, pmob=pmob,
                    gender=gender, add=add, code=code, class_obj=class_instance,
                    pas=pas, bod=bod, state=state_instance, city=city_instance, area=area_instance,image=image
                )

                return render(request, 'Admission.html', {
                    'store': 'Registration successful',
                    'cls': clas,
                    'states': states,
                    'selected_state': selected_state,
                    'selected_city': selected_city
                })
        else:
            return render(request, 'Admission.html', {
                'error': 'Both passwords must be the same',
                'cls': clas,
                'states': states,
                'cities': cities,
                'areas': areas,
                'selected_state': selected_state,
                'selected_city': selected_city
            })

    return render(request, 'Admission.html', {
        'cls': clas,
        'states': states,
        'cities': cities,
        'areas': areas,
        'selected_state': selected_state,
        'selected_city': selected_city
    })


# -------
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_API_SECRET))

def approve_student(request, inquiry_id):
    inquirys = get_object_or_404(inquiry, id=inquiry_id)
    inquirys.status = "Approved"
    inquirys.save()
    
    
    # Add the student to the Student table
    # students = student.objects.create(name=inquirys.name, email=inquirys.email, mob=inquirys.mob, class_obj=inquirys.class_obj,)

    # Send email with payment link
    payment_url = f"http://127.0.0.1:8000/payment/{inquirys.id}"
    send_mail(
        subject="Registration Approved",
        message=f"Dear {inquirys.name}, your registration is approved. Please complete your payment here: {payment_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[inquirys.email],
    )
    return redirect("admin_dashboard")

def delete_istudent(request, istudent_id):
    Student = get_object_or_404(inquiry, id=istudent_id)

    if request.method == "POST":
        Student.delete()
        return redirect("admin_view__student")  # Redirect after deletion

    return render(request, "delete_istudent.html", {"student": Student})

# ---------teacher approve send email with login--------------


def teacherpersonal(request):
    
    subjects = Subjects.objects.all()
    

    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        mob = request.POST.get('phoneNo')
        gender = request.POST.get('gender')
        pas = request.POST.get('pas')
        add = request.POST.get('address')
        qualification = request.POST.get('qulification')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        image = request.FILES.get('image')
        # class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject_id')

        # Check if the teacher is already registered
        if teacher.objects.filter(email=email).exists():
            return render(request, 'TeacherPersonal.html', {'al': 'already registered'})

        # Validate passwords
        if pas == request.POST.get('cpas'):
            if all([name, email, mob, qualification, specialization, experience, pas,  add, gender, subject_id,image]):
                # class_obj = get_object_or_404(Class, id=class_id)
                subject_obj = get_object_or_404(Subjects, id=subject_id)

                # Create the teacher record
                new_teacher = teacher.objects.create(
                    name=name, email=email, mob=mob, qulification=qualification,
                    specialization=specialization, experience=experience, gender=gender,
                    add=add, pas=pas,
                    Subjects_obj=subject_obj,image=image
                )

                # Send email notification to admin
                admin_email = "rpatel17381@gmail.com"  # Replace with actual admin email
                subject = "New Teacher Registration Alert"
                message = f"""
                A new teacher has registered. Please review the details in the dashboard.
                
                Name: {name}
                Email: {email}
                Mobile: {mob}
                Qualification: {qualification}
                Specialization: {specialization}
                Experience: {experience}
                # Class Assigned:
                 {new_teacher.Class_obj.name}
                Subject Assigned: {subject_obj.sub_name}

                Please log in to the admin panel to verify the details.
                """
                send_mail(subject, message, "rpatel17381@gmail.com", [admin_email], fail_silently=False)

                return render(request, 'TeacherPersonal.html', {'store': 'Registration successful. Admin has been notified.'})
            else:
                return render(request, 'TeacherPersonal.html', {'error': 'All fields are required'})
        else:
            return render(request, 'TeacherPersonal.html', {'error': 'Both passwords must be the same'})

    return render(request, 'TeacherPersonal.html', {
        # 'class': classes,
        'subject': subjects
        # 'selected_class': selected_class
    })

  # Import the necessary models



def approve_teacher(request, teacher_id):
    inquirys = get_object_or_404(teacher, id=teacher_id)
    classes = Class.objects.all()  # Fetch all available classes

    if request.method == "POST":
        class_id = request.POST.get("class_id")

        if not class_id:
            return render(request, "approve_teacher.html", {
                "teacher": inquirys,
                "classes": classes,
                "error": "Please select a class before approving.",
            })

        # Assign the selected class
        class_obj = get_object_or_404(Class, id=class_id)
        inquirys.Class_obj = class_obj  # Assign class to teacher
        inquirys.status = "Approved"
        inquirys.save()

        # Store in ApproveTeacher model
        approveteacher.objects.create(
            name=inquirys.name,
            email=inquirys.email,
            mob=inquirys.mob,
            gender=inquirys.gender,
            add=inquirys.add,
            pas=inquirys.pas,
            qulification=inquirys.qulification,
            specialization=inquirys.specialization,
            experience=inquirys.experience,
            Class_obj=class_obj,  # Assign selected class
            Subjects=inquirys.Subjects_obj,
            image=inquirys.image # Store assigned subject
        )

        # Send email confirmation
        payment_url = "http://127.0.0.1:8000/tutorLogin/"
        send_mail(
            subject="Your Approval Confirmation",
            message=f"Dear {inquirys.name}, you are approved for {inquirys.Subjects_obj.sub_name} in  {class_obj.name}. \n Login here: {payment_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[inquirys.email],
        )

        return redirect("admin_dashboard")  # Redirect after approval

    return render(request, "approve_teacher.html", {
        "teacher": inquirys,
        "classes": classes,
    })


def Logintutor(request):
    if request.method =="POST":
        try:
            useremail=teacher.objects.get(email=request.POST['email'])
            
            # print(useremail.name,useremail.pas)
            if useremail.pas == request.POST['password']:
               request.session['email']=useremail.email
               return redirect('teacher_dashboard')
            
            else:
               return render(request,'teacher_login.html',{'error':"password wrong"})
        except:
                return render(request,'teacher_login.html',{'nr':"not register or you are not teacher"})
    else:
        return render(request,'teacher_login.html')
    
def teacher_profile(request):
    if 'email' in request.session:  # Check if the student is logged in
        try:
            # Retrieve student details using the email stored in the session
            user_email = request.session['email']
            teacher_data =approveteacher.objects.get(email=user_email)

            # Pass the student details to the dashboard template
            return render(request, 'tutor_profile.html', {'teacherpersonal': teacher_data})

        except teacher.DoesNotExist:
            # If the student record does not exist, clear session and redirect to login
            del request.session['email']
            return redirect('Logintutor')
    else:
        # If session does not exist, redirect to login
        return redirect('home')
    
def tutor(request):
        # Fetch all payments with status = True
    approve_teacher = teacher.objects.filter(status='Approved')
    
    for tutor in approve_teacher:
        registration = tutor
        print(registration)
        # Ensure this retrieves the related Registration object
        # Check if the student already exists
        if not approveteacher.objects.filter(email=registration.email).exists():
            # Create a new student record
            approveteacher.objects.create(
                name=registration.name,
                email=registration.email,
                gender=registration.gender,
                mob=registration.mob,
                qulification=registration.qulification,
                pas=registration.pas,
                add= registration.add,
                Subjects=registration.Subjects_obj,
                Class_obj=registration.Class_obj,
                specialization=registration.specialization,
                experience=registration.experience,
                image=registration.image

            )

       
    return redirect(approvet_teacher_detail)
   
def update_teacher(request, teacher_id):
    teacher = get_object_or_404(approveteacher, id=teacher_id)  # Fetch teacher object
    subjects = Subjects.objects.all()  # Fetch all subjects

    if request.method == "POST":
        teacher.name = request.POST.get("name")
        teacher.email = request.POST.get("email")
        teacher.mob = request.POST.get("mod")
        teacher.add = request.POST.get("add")

        class_id = request.POST.get("class_obj")  # Get selected subject ID
        print(teacher.name,teacher.email,teacher.mob,teacher.add,class_id)
        if class_id:  # Ensure subject ID is selected
            teacher.Subjects = get_object_or_404(Subjects, id=class_id)  # Assign subject

        teacher.save()  # Save updated teacher details
        return redirect("approvet_teacher_detail")  # Redirect after update

    return render(request, "update_teacher.html", {"student": teacher, "subjects": subjects})

def delete_teacher(request, teacher_id):
    Student = get_object_or_404(approveteacher, id=teacher_id)

    if request.method == "POST":
        Student.delete()
        return redirect("approvet_teacher_detail")  # Redirect after deletion

    return render(request, "delete_teacher.html", {"student": Student})

def delete_iteacher(request, iteacher_id):
    Student = get_object_or_404(teacher, id=iteacher_id)

    if request.method == "POST":
        Student.delete()
        return redirect("view_teacher")  # Redirect after deletion

    return render(request, "delete_iteacher.html", {"student": Student})

def view_sm(request):
    if 'email' in request.session:  # Checking if the user is logged in
        teacher_email = request.session['email']  # Get logged-in teacher's email
        
        # Get the teacher's assigned class
        assigned_class = approveteacher.objects.filter(email=teacher_email).values_list('Class_obj', flat=True)

        # Filter study materials based on the assigned class
        sm = Study_Material.objects.filter(class_obj__in=assigned_class)

        return render(request, 'view_sm.html', {'materials': sm})
    else:
        return redirect('login')

def teacher_view_exam(request):
    if 'email' in request.session:  # Checking if the user is logged in
        teacher_email = request.session['email']  # Get logged-in teacher's email
        
        # Get the teacher's assigned class
        assigned_classes = approveteacher.objects.filter(email=teacher_email).values_list('Class_obj', flat=True)

        selected_class_id = request.GET.get('class_id', None)  # Get selected class
        selected_exam_name = request.GET.get('exam_name', None)  # Get selected exam

        # Filter classes based on teacher's assigned class
        classes = Class.objects.filter(id__in=assigned_classes)

        exams = []  # List to store exam names for selected class
        timetables = []  # List to store exam timetable details

        if selected_class_id and int(selected_class_id) in assigned_classes:
            # Get distinct exam names for the selected class
            exams = exam_time_table.objects.filter(Class_obj_id=selected_class_id).values_list('exam_name', flat=True).distinct()
            
            if selected_exam_name:
                # Get the timetable details for the selected exam in the selected class
                timetables = exam_time_table.objects.filter(Class_obj_id=selected_class_id, exam_name=selected_exam_name)

        return render(request, 'teacher_view_exam.html', {
            'classes': classes,
            'exams': exams,
            'timetables': timetables,
            'selected_class_id': selected_class_id,
            'selected_exam_name': selected_exam_name
        })
    else:
        return redirect('login')  # Redirect to login if not logged in


def teacher_batch_timetable(request):
    if 'email' in request.session:  # Ensure the user is logged in
        teacher_email = request.session['email']  # Get logged-in teacher's email

        # Get assigned classes for the teacher
        assigned_classes = approveteacher.objects.filter(email=teacher_email).values_list('Class_obj', flat=True)

        # Fetch only the assigned classes
        classes = Class.objects.filter(id__in=assigned_classes)

        selected_class_id = request.GET.get('class_id')
        selected_batch_id = request.GET.get('batch_id')

        # Convert `selected_class_id` to int if it exists and ensure it's a valid assigned class
        if selected_class_id:
            try:
                selected_class_id = int(selected_class_id)
                if selected_class_id not in assigned_classes:
                    selected_class_id = None  # Reset if unauthorized
            except ValueError:
                selected_class_id = None

        # Fetch batches based on selected class
        batches = division.objects.filter(class_obj_id=selected_class_id) if selected_class_id else division.objects.none()

        # Days of the week for table headers
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Fetch timetable entries only if the selected batch belongs to the selected class
        timetable_entries = []
        if selected_batch_id and selected_class_id:
            try:
                selected_batch_id = int(selected_batch_id)
                timetable_entries = batch_time_table.objects.filter(batch_obj_id=selected_batch_id, class_obj_id=selected_class_id)
            except ValueError:
                timetable_entries = []

        # Structure the timetable by time slot
        structured_timetable = {}
        for entry in timetable_entries:
            time_slot = f"{entry.time} - {entry.e_time}"
            if time_slot not in structured_timetable:
                structured_timetable[time_slot] = {day: "" for day in days_of_week}
            
            structured_timetable[time_slot][entry.day] = entry.Subjects_obj.sub_name

        return render(request, 'teacher_view_batchtimetable.html', {
            'classes': classes,
            'batches': batches,
            'timetable_entries': timetable_entries,
            'structured_timetable': structured_timetable,
            'days_of_week': days_of_week,
            'selected_class_id': selected_class_id,
            'selected_batch_id': selected_batch_id,
        })
    else:
        return redirect('login')   # Redirect to login if not authenticated


def teacher_view_quizzes(request):
    if 'email' not in request.session:
        return redirect('login')  # Ensure user is logged in

    teacher_email = request.session['email']
    
    # Get teacher's assigned classes from ApproveTeacher
    teacher = get_object_or_404(approveteacher,email=teacher_email)
    assigned_classes = approveteacher.objects.filter(name=teacher.name).values_list('Class_obj', flat=True)

    # Get only quizzes related to the assigned classes
    quizzes = Quiz.objects.filter(class_obj_id__in=assigned_classes)

    return render(request, "teacher_view_quiz.html", {"quizzes": quizzes})

# ---------- staff teacher approve send email with login-----------

def Staffpersonal(request):
    if request.method=="POST":
        s=staff()
        s.name=request.POST['name']
        s.email=request.POST['email']
        s.mob=request.POST['phoneNo']
       
        s.gender=request.POST.get('gender')
        s.add=request.POST['address']
        s.pas=request.POST['pas']
        s.qulification=request.POST['qulification']
        s.specialization=request.POST['specialization']
        s.experience=request.POST['experience']
        s.image = request.FILES.get('image')
       
        
        alregi=staff.objects.filter(email=request.POST['email'])
        if alregi:
            return render(request,'StaffPersonal.html',{'al':'already regi'})
        else:
            if request.POST['pas'] == request.POST['cpas']:
                s.save()
                admin_email = "rpatel17381@gmail.com"  # Replace with actual admin email
                subject = "New Staff Registration Alert"
                message = f"""
            A new staff member has registered. Please review the details in the dashboard.
            
            Name: {s.name}
            Email: {s.email}
            Mobile: {s.mob}
            Qualification: {s.qulification}
            Specialization: {s.specialization}
            Experience: {s.experience}
            

            Please log in to the admin panel to verify the details.
            """
                send_mail(subject, message, "rpatel17381@gmail.com", [admin_email], fail_silently=False)
                return render(request,'StaffPersonal.html',{'store':'regi sucess.Admin has been notified.'})
            else:
                return render(request,'StaffPersonal.html',{'error':'both password must be same'})
    else:
        return render(request,'StaffPersonal.html')

def approve_staff(request, staff_id):
    inquirys = get_object_or_404(staff, id=staff_id)
    inquirys.status = "Approved"
    inquirys.save()
    
    
    # Add the student to the Student table
    # students = student.objects.create(name=inquirys.name, email=inquirys.email, mob=inquirys.mob, class_obj=inquirys.class_obj,)

    # Send email with payment link
    payment_url = f"http://127.0.0.1:8000/Loginstaff/"
    send_mail(
        subject="Registration Approved",
        message=f"Dear {inquirys.name}, your staff post is approved.  {payment_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[inquirys.email],
    )
    return redirect("admin_dashboard")

def Loginstaff(request):
    if request.method =="POST":
        try:
            useremail=staff.objects.get(email=request.POST['email'])
            
            # print(useremail.name,useremail.pas)
            if useremail.pas == request.POST['password']:
               request.session['email']=useremail.email
               return redirect('staff_dashboard')
            
            else:
               return render(request,'staff_login.html',{'error':"password wrong"})
        except:
                return render(request,'staff_login.html',{'nr':"not register or you are not teacher"})
    else:
        return render(request,'staff_login.html')


def staff_profile(request):
    if 'email' in request.session:  # Check if the student is logged in
        try:
            # Retrieve student details using the email stored in the session
            user_email = request.session['email']
            teacher_data = staff.objects.get(email=user_email)

            # Pass the student details to the dashboard template
            return render(request, 'staff_profile.html', {'teacherpersonal': teacher_data})

        except teacher.DoesNotExist:
            # If the student record does not exist, clear session and redirect to login
            del request.session['email']
            return redirect('Loginstaff')
    else:
        # If session does not exist, redirect to login
        return redirect('home')
    
def staff_details(request):
        # Fetch all payments with status = True
    approve_teacher = staff.objects.filter(status='Approved')
    
    for tutor in approve_teacher:
        registration = tutor
        print(registration)
        # Ensure this retrieves the related Registration object
        # Check if the student already exists
        if not approvestaff.objects.filter(email=registration.email).exists():
            # Create a new student record
            approvestaff.objects.create(
                # user=request.user,
                name=registration.name,
                email=registration.email,
                gender=registration.gender,
                mob=registration.mob,
                qulification=registration.qulification,
                pas=registration.pas,
                add= registration.add,
                image=registration.image,
                specialization=registration.specialization,
                experience=registration.experience
              

            )

       
    return redirect(approvet_staff_detail)

def update_staff(request, staff_id):
    students = get_object_or_404(approvestaff, id=staff_id)
    clas=Subjects.objects.all()

    if request.method == "POST":
        students.name = request.POST.get("name")
        students.email = request.POST.get("email")
        students.mob = request.POST.get("mob")
        students.add = request.POST.get("add")
       
        
        students.save()
        return redirect("approvet_staff_detail")  # Redirect to the student list page

    return render(request, "update_staff.html", {"student": students,'classes':clas})

def delete_staff(request, staff_id):
    Student = get_object_or_404(approvestaff, id=staff_id)

    if request.method == "POST":
        Student.delete()
        return redirect("approvet_staff_detail")  # Redirect after deletion

    return render(request, "delete_staff.html", {"student": Student})

def delete_istaff(request, istaff_id):
    Student = get_object_or_404(staff, id=istaff_id)

    if request.method == "POST":
        Student.delete()
        return redirect("view_staff")  # Redirect after deletion

    return render(request, "delete_istaff.html", {"student": Student})
  
# ----------admin dashboard----

def admin_dashboard(request):
   
    n=notice.objects.all()
    return render(request, "a.html", {
        'no':n
    })


def admin_dashboard2(request):
    total_students = student.objects.count()
    total_t = approveteacher.objects.count()
    total_st = staff.objects.count()
    total_fees_collected = pay.objects.aggregate(total_fees=models.Sum('amount'))['total_fees'] or 0
    return render(request, "admin_dashboard.html", {
        "total_students": total_students,
        "total_fees_collected": total_fees_collected,
        "total_st":total_st,
        "total_t":total_t


    })  

def admin_profile(request):
   return render(request, "admin_profile.html") 

def adminmanage(request):
    return render(request,'admin_manage.html')

def adminlogin(request):
    if request.method =="POST":
        try:
            useremail=Author.objects.get(email=request.POST['email'])
            # print(useremail.name,useremail.pas)
            if useremail.pas == request.POST['password']:
               request.session['email']=useremail.email
               return redirect('admin_dashboard')
            
            else:
               return render(request,'admin_login.html',{'error':"password wrong"})
        except:
                return render(request,'admin_login.html',{'nr':"not register or you are not teacher"})
    else:
        return render(request,'admin_login.html')

def admin_view_mark(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class_id')  
    selected_exam = request.GET.get('exam_id')  

    exams = []
    students_marks = []

    if selected_class:
        exams =exam_time_table.objects.filter(Class_obj_id=selected_class)

    if selected_exam:
        students_marks = Marks.objects.filter(exam_obj_id=selected_exam).select_related('student_obj')

    return render(request, 'admin_view_mark.html', {
        'classes': classes,
        'exams': exams,
        'students_marks': students_marks,
        'selected_class': selected_class,
        'selected_exam': selected_exam
    })



def admin_view_batch_wise_attendance(request):
    batches = division.objects.all()  # Fetch all batches
    selected_batch = request.GET.get('batch_id')  # Get selected batch from dropdown
    attendance_records = None  

    if selected_batch:
        students = student.objects.filter(batch=selected_batch)  # Get students in batch
        attendance_records = Attendance.objects.filter(student__in=students).order_by('-date')

    return render(request, 'admin_view_attendance.html', {
        'batches': batches,
        'attendance_records': attendance_records,
        'selected_batch': selected_batch
    })


# --------------fee-------------

def admin_fee(request):
    clas=Class.objects.all()
    if request.method=='POST':
        class_id = request.POST.get('select')
        name = request.POST.get('name')

        if class_id and name:
            class_instance = Class.objects.get(id=class_id)
            Fee.objects.create(class_related =class_instance,amount=name)
            return render(request,'admin_view_fee.html',{'sucessfully':'sucessfully store'})
    else:
       return render(request,'admin_view_fee.html',{'cls':clas})


def view_fee_detail(request):
    selected_class_id = request.GET.get('class_id', None)
    classes = Class.objects.all()
    f = Fee.objects.filter(class_related=selected_class_id) if selected_class_id else None
    return render(request, 'view_fees.html', {
        'class': classes,
        'fee':f,
        'selected_class_id': selected_class_id
    })
    

def update_fee(request, fee_id):
    students = get_object_or_404(Fee, id=fee_id)
    clas=Class.objects.all()

    if request.method == "POST":
        students.amount = request.POST.get("name")
        class_id = request.POST.get("class_obj")
        if class_id:
            students.class_related = get_object_or_404(Class, id=class_id) # Ensure ID is passed
        students.save()
        return redirect("view_fee_detail")  # Redirect to the student list page

    return render(request, "update_fee.html", {"student": students,'classes':clas})

def delete_fee(request,fee_id):
    Student = get_object_or_404(Fee, id=fee_id)

    if request.method == "POST":
        Student.delete()
        return redirect("view_fee_detail")  # Redirect after deletion

    return render(request, "confirm_delete_fee_detail.html", {"student": Student})


# ----------teacher dashboard--------

def teacher_dashboard(request):
   if 'email' in request.session:
       return render(request, 'teacher_dashboard.html',{'session':True})
   else:
       return redirect('home')

def admin_teacher(request):
    return render(request,'admin_teacher.html')

def viewteacher(request):
    tutor=teacher.objects.all()
    return render(request,'admin_view_teacher.html',{'t1':tutor})

def approvet_teacher_detail(request):
    tutor=approveteacher.objects.all()
    return render(request,'admin_view_approvetutor.html',{'stu':tutor})

# -------------------staff dashboard----------------

def staff_dashboard(request):
   n=notice.objects.all()
   if 'email' in request.session:
       return render(request, 'staff_dashboard.html',{'no':n,'session':True})
   else:
       return redirect('home')
   
def approvet_staff_detail(request):
    tutor=approvestaff.objects.all()
    return render(request,'admin_view_approvestaff.html',{'stu':tutor})

def admin_staff(request):
    return render(request,'admin_staff.html')

def viewstaff(request):
    staffs=staff.objects.all()
    return render(request,'view_staff.html',{'t1':staffs})

# --------------student dashboard---------

def student_dashboard(request):
   n=notice.objects.all()
   if 'email' in request.session:
       return render(request, 'student_dashboard.html',{'no':n,'session':True})
   else:
       return redirect('home')

def admin_student(request):
   return render(request, "admin_student.html")

def inquirystudent(request):
    Inquiry=inquiry.objects.all()
    return render(request,'admin_view_student.html',{'stu':Inquiry})


def pay_student(request):
        # Fetch all payments with status = True
    successful_payments = pay.objects.filter(status=True)
    
    for payment in successful_payments:
        registration = payment.student_name
        # Ensure this retrieves the related Registration object
        # Check if the student already exists
        if not student.objects.filter(email=registration.email).exists():
            # Create a new student record
            student.objects.create(
                name=registration.name,
                email=registration.email,
                gender=registration.gender,
                mob=registration.mob,
                pmob=registration.pmob,
                pas=registration.pas,
                add= registration.add,
                class_obj=registration.class_obj,
                amount=payment.amount,
                image=registration.image
              

            )
    return redirect('viewpay_student')

       

def paystudent(request):
    Inquiry=student.objects.all()
    return render(request,'admin_view_paystu.html',{'stu':Inquiry})

def send_studentlogin(request, student_id):
    stu = get_object_or_404(student, id=student_id)
    stu.status = "sent"
    stu.save()
    
    
    # Add the student to the Student table
    # students = student.objects.create(name=inquirys.name, email=inquirys.email, mob=inquirys.mob, class_obj=inquirys.class_obj,)

    # Send email with payment link
    subject = "Your Login Credentials"
    message = f"""
    Hello {stu.name},

    Your login credentials are:
    Email: {stu.email}
    Password: {stu.pas} 

    Click the link below to log in:
    {request.build_absolute_uri('/Login/')}
    """
    send_mail(
        subject,
        message,
        'rpatel17381@gmail.com',  # Replace with your email
        [stu.email],
    )
    return redirect("admin_dashboard")

def Login(request):
    if request.method =="POST":
        try:
            useremail=student.objects.get(email=request.POST['email'])
            
            # print(useremail.name,useremail.pas)
            if useremail.pas == request.POST['password']:
               request.session['email']=useremail.email
               return redirect('student_dashboard')
            
            else:
               return render(request,'Login.html',{'error':"password wrong"})
        except:
                return render(request,'Login.html',{'nr':"not register"})
    else:
        return render(request,'Login.html')
    



def student_profile(request):
    if 'email' in request.session:  # Check if the student is logged in
        try:
            # Retrieve student details using the email stored in the session
            user_email = request.session['email']
            student_data = student.objects.get(email=user_email)

            # Pass the student details to the dashboard template
            return render(request, 'stu_profile.html', {'Inquiry': student_data})

        except student.DoesNotExist:
            # If the student record does not exist, clear session and redirect to login
            del request.session['email']
            return redirect('send_studentlogin')
    else:
        # If session does not exist, redirect to login
        return redirect('home')

def update_student(request, student_id):
    students = get_object_or_404(student, id=student_id)
    clas=Class.objects.all()

    if request.method == "POST":
        students.name = request.POST.get("name")
        students.email = request.POST.get("email")
        students.mob = request.POST.get("mob")
        class_id = request.POST.get("class_obj")
        if class_id:
            students.class_obj = get_object_or_404(Class, id=class_id) # Ensure ID is passed
        students.save()
        return redirect("viewpay_student")  # Redirect to the student list page

    return render(request, "update_student.html", {"student": students,'classes':clas})

def delete_student(request, student_id):
    Student = get_object_or_404(student, id=student_id)

    if request.method == "POST":
        Student.delete()
        return redirect("viewpay_student")  # Redirect after deletion

    return render(request, "confirm_delete.html", {"student": Student})


def student_timetable(request):
 if 'email' in request.session:
        user_email = request.session['email']  # Get logged-in student's email
        timetable_entries = None  # Default value if no batch is found

        try:
            student_data = student.objects.get(email=user_email)  # Get student data
            timetable_entries = batch_time_table.objects.filter(batch_obj=student_data.batch)  # Get timetable for batch
        except student.DoesNotExist:
            timetable_entries = None  # If no student record is found

        # Structure timetable data for display
        structured_timetable = {}
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        if timetable_entries:
            for entry in timetable_entries:
                time_slot = f"{entry.time} - {entry.e_time}"  # Format time slot

                if time_slot not in structured_timetable:
                    structured_timetable[time_slot] = {}

                structured_timetable[time_slot][entry.day] = entry  # Store the full timetable entry

        return render(request, 'student_timetable.html', {
            'structured_timetable': structured_timetable,
            'days_of_week': days_of_week
        })

 return render(request, 'student_timetable.html', {'structured_timetable': None})
def student_examtimetable(request):
    if 'email' in request.session:
        user_email = request.session['email']  # Assuming user is logged in
        timetables = None  # Default value if no batch found

        try:
            exams = []  # List to store exam names for selected class
            timetables = [] 
            student_data = student.objects.get(email=user_email)  # Get student inquiry record
            selected_exam_name = request.GET.get('exam_name', None)  
            exams = exam_time_table.objects.filter(Class_obj=student_data.class_obj).values_list('exam_name', flat=True).distinct()
        
            if selected_exam_name:
            # Get the timetable details for the selected exam in the selected class
                timetables = exam_time_table.objects.filter(Class_obj_id=student_data.class_obj, exam_name=selected_exam_name)

            # Get batch timetable
        except inquiry.DoesNotExist:
            timetables = None  # If no inquiry is found, show no timetable

    return render(request, 'student_examtimetable.html', {
        't': timetables,
        'exams':exams
    })

def student_mark(request):
    if 'email' in request.session:
        user_email = request.session['email']  # Get logged-in student's email
        student_marks = None  # Default value if no marks found

        try:
            student_data = student.objects.get(email=user_email)  # Get student record
            student_marks = Marks.objects.filter(student_obj=student_data)  # Get only the logged-in student's marks
        except student.DoesNotExist:
            student_marks = None  # If no student record is found

        return render(request, 'student_view_mark.html', {
            'marks': student_marks
        })

    return render(request, 'student_view_mark.html', {'marks': None})

def student_studymaterial(request):
 if 'email' in request.session:
    user_email = request.session['email']  # Assuming user is logged in
    materials = None  # Default value if no class found

    try:
        student_data = student.objects.get(email=user_email)  
        current_class = student_data.class_obj  # Get student data
        print(current_class)
        materials = Study_Material.objects.filter(class_obj=current_class)  
        
    except student.DoesNotExist:
        materials = None  # If no student is found, show no materials

 return render(request, 'student_view_sm.html', {
    'materials': materials
})


def student_attendance(request):
    if 'email' in request.session:  
        user_email = request.session['email']  # Get logged-in student's email
        attendance_records = None  # Default to None if no records found

        try:
            student_data = student.objects.get(email=user_email)  # Get student record
            attendance_records = Attendance.objects.filter(student=student_data).order_by('-date')  
        except student.DoesNotExist:
            attendance_records = None  # If no student is found, show nothing

    return render(request, 'student_view_attendance.html', {'attendance_records': attendance_records})

def student_quiz(request):
    if 'email' in request.session:
        user_email = request.session['email']  # Assuming user is logged in
        timetable = None  # Default value if no batch found

        try:
            student_data = student.objects.get(email=user_email)  # Get student inquiry record
            timetable =batch_time_table.objects.filter(batch_obj=student_data.batch)  
            print(timetable)
            # Get batch timetable
        except inquiry.DoesNotExist:
            timetable = None  # If no inquiry is found, show no timetable

    return render(request, 'student_timetable.html', {
        't': timetable
    })

#  ---------------------notice------------------

def notices(request):
    if request.method=='POST':
        date=request.POST.get('date')
        title=request.POST.get('name')
        msg=request.POST.get('tname')

        if date and title and msg:
            # Save the notice
            notices = notice.objects.create(name=title, msg=msg,date=date)
            
            # Fetch all students' emails
            students = student.objects.values_list('email', flat=True)
            
            # Send email to all students
            subject = "New Notice Available"
            message = f"A new notice has been posted:\n\nTitle: {title}\n\n{msg}\n\nPlease check the notice section for details."
            from_email = "rpatel17381@gmail.com"  # Replace with your email
            recipient_list = list(students)

            if recipient_list:  # Send email only if students exist
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

             # Change to your actual notice listing page
            return render(request,'admin_notice.html',{'sucessfully':'sucessfully store'})
    else:
        return render(request,'admin_notice.html',)

def view_notices(request):
    notices = notice.objects.all().order_by('-id')  # Fetch all notices, latest first
    return render(request, "view_notice.html", {"notices": notices})

def aview_notices(request):
    notices = notice.objects.all().order_by('-id')  # Fetch all notices, latest first
    return render(request, "all_view_notice.html", {"notices": notices})


def delete_notice(request, notice_id):
    Student = get_object_or_404(notice, id=notice_id)

    if request.method == "POST":
        Student.delete()
        return redirect("view_notices")  # Redirect after deletion

    return render(request, "delete_notice.html", {"student": Student})
# ----------------batch--------
def add_batch(request):
    clas=Class.objects.all()
    if request.method=='POST':
        class_id = request.POST.get('select')
        batch_name = request.POST.get('batchname')
        already=division.objects.filter(name=batch_name)
        if already:
            return render(request,'batch_add.html',{'exit':'already exits'})
        if class_id and batch_name:
            class_instance = Class.objects.get(id=class_id)
            division.objects.create(class_obj=class_instance,name=batch_name)
            return render(request,'batch_add.html',{'sucessfully':'sucessfully store'})
        else:
            return render(request,'batch_add.html',{'error':'All feild are required! Please enter First'})
    else:
        return render(request,'batch_add.html',{'cls':clas})

def view_batch(request):
    selected_class_id = request.GET.get('class_id')

    if selected_class_id:
        try:
            selected_class_id = int(selected_class_id)  # Convert to integer
        except ValueError:
            selected_class_id = None 

    classes = Class.objects.all()

    # 🛠 Fix: Ensure correct filtering
    divisions = division.objects.filter(class_obj_id=selected_class_id) if selected_class_id else []

    return render(request, 'view_batch.html', {
        'classes': classes,  
        'div': divisions,  
        'selected_class_id': selected_class_id
    })


    # return render(request,'view_batch.html',{'batch':b})

def update_batch(request, batch_id):
    students = get_object_or_404(division, id=batch_id)
    clas=Class.objects.all()

    if request.method == "POST":
        students.name = request.POST.get("name")
        class_id = request.POST.get("class_obj")
        
        if class_id:
            students.class_obj = get_object_or_404(Class, id=class_id) # Ensure ID is passed
        students.save()
        return redirect("batch_view")  # Redirect to the student list page

    return render(request, "update_batch.html", {"student": students,'classes':clas})

def delete_batch(request, batch_id):
    Student = get_object_or_404(division, id=batch_id)

    if request.method == "POST":
        Student.delete()
        return redirect("batch_view")  # Redirect after deletion

    return render(request, "confirm_delete_batch.html", {"student": Student})

# --------------class----------------

def add_class(request):
     if request.method=='POST':
        Clss=Class()
        Clss.name=request.POST['classname']
        already=Class.objects.filter(name=Clss.name)
        if already:
            return render(request,'add_class.html',{'exit':'already exits'})
        # Clss = Class(name=Clss.name)
        Clss.save()
        return render(request,'add_class.html',{'sucessfully':'sucessfully store'})
     else:
         return render(request,'add_class.html')
         
def view_class(request):
    c=Class.objects.all()
    return render(request,'view_class.html',{'Class':c})

def update_class(request, class_id):
    students = get_object_or_404(Class, id=class_id)

    if request.method == "POST":
        new_name = request.POST.get("name")  # Get new class name

        # Check if class name already exists but exclude current class
        already_exists = Class.objects.filter(name=new_name).exclude(id=class_id).exists()
        
        if already_exists:
            return render(request, 'update_class.html', {'exit': 'Already exists', "student": students})

        students.name = new_name
        students.save()
        division.objects.filter(class_obj=students).update(class_obj=students)

        return redirect("class_view")  # Redirect to class view page

    return render(request, "update_class.html", {"student": students})

def delete_class(request, class_id):
    Student = get_object_or_404(Class, id=class_id)
    if request.method == "POST":
        Student.delete()
        return redirect("class_view")  # Redirect after deletion

    return render(request, "confirm_delete_class.html", {"student": Student})

# ---------------------gallery--------------

def add_gallery(request):
   if request.method=='POST':
        g=gallery()
        g.image = request.FILES.get('image')
        g.year = request.POST.get('year')
        g.save()
        return render(request,'manage_gallery.html',{'sucessfully':'sucessfully store'})
   else:
        return render(request, "manage_gallery.html") 



def view_gallery(request):
   
    Division = gallery.objects.all()
    return render(request, 'view_gallery.html', {
        'subjects': Division,
        
    })
    

def update_gallery(request, gallery_id):
    subject = get_object_or_404(gallery, id=gallery_id)
    
    if request.method == 'POST' and request.FILES.get('image'):
        subject.year=request.POST.get('year')
        subject.image = request.FILES['image']  # Assign the new image
        subject.save()
        return redirect('view_gallery')  # Redirect to a page after updating

    return render(request, 'update_gallery.html', {'subjects': subject})

def delete_gallery(request, gallery_id):
    subject = get_object_or_404(gallery, id=gallery_id)
    if request.method == "POST":
        subject.delete()
        return redirect("view_gallery") 
    return render(request, 'delete_gallery.html', {'subject': subject})
    
    
# -----------------------study material----------------

def add_sm(request):
     if 'email' in request.session:  # Check if the student is logged in
        try:
            # Retrieve student details using the email stored in the session
            user_email = request.session['email']
            teacher_data = approveteacher.objects.get(email=user_email)

            # Pass the student details to the dashboard template
            if request.method=='POST':
            #    date = request.POST.get('Date')
               uploaded_file = request.FILES.get('pdf_url')
            
               if uploaded_file and teacher_data :
                   try:
                        print(uploaded_file,teacher_data )
                        # class_instance = approveteacher.objects.get(id=teacher_id)
                        Study_Material.objects.create(teacher_obj=teacher_data,  pdf_url=uploaded_file,class_obj=teacher_data.Class_obj)
                        return render(request, 'manage_sm.html', {'success': 'Successfully stored', 'teacher':teacher_data.Class_obj})
                   except approveteacher.DoesNotExist:
                        return render(request, "manage_sm.html", {'error': 'Teacher not found', 'teacher': teacher_data.Class_obj})
            return render(request, "manage_sm.html", {'teacher': teacher_data.Class_obj})
        except student.DoesNotExist:
            # If the student record does not exist, clear session and redirect to login
            del request.session['email']
            return redirect('logintutor')
        # If form is incomplete, return an error message
               
     else:
            return render(request, "manage_sm.html") 


def update_sm(request, sm_id):
    subject = get_object_or_404(Study_Material, id=sm_id)
    clas=approveteacher.objects.all()
    if request.method == 'POST' and request.FILES.get('image'):
        subject.date=request.POST.get('date')
        subject.pdf_url = request.FILES['image'] 
        class_id = request.POST.get("class_obj")
        if class_id:
            subject.teacher_obj = get_object_or_404(approveteacher, id=class_id) # Ensure ID is passed # Assign the new image
        subject.save()
        return redirect('view_sm')  # Redirect to a page after updating

    return render(request, 'update_sm.html', {'subjects': subject,'class':clas})

def delete_sm(request, sm_id):
    subject = get_object_or_404(Study_Material, id=sm_id)
    if request.method == "POST":
        subject.delete()
        return redirect("view_sm") 
    return render(request, 'delete_sm.html', {'subject': subject})
    

# ------------------marks------------------------

from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, student, exam_time_table, Marks

def add_mark(request):
    selected_class_id = request.GET.get('class_id', None)
    selected_exam_id = request.GET.get('exam_id', None)

    classes = Class.objects.all()
    students = []
    exams = []
    selected_exam = None

    if selected_class_id:
        students = student.objects.filter(class_obj_id=selected_class_id)  # Fetch students of selected class
        exams = exam_time_table.objects.filter(Class_obj_id=selected_class_id)  # Fetch exams for selected class

        if selected_exam_id:
            selected_exam = get_object_or_404(exam_time_table, id=selected_exam_id)
    
    # If form is submitted, save marks for all students
    if request.method == "POST":
        exam_id = request.POST.get('exam_id')
        exam_obj = exam_time_table.objects.get(id=exam_id)

        for student_obj in students:
            marks = request.POST.get(f'marks_{student_obj.id}')  # Fetch marks for each student

            if marks:  # Check if marks were entered
                marks = int(marks)  # Convert to integer

                # ✅ Check if marks already exist for the student & exam
                mark_entry, created = Marks.objects.get_or_create(
                    student_obj=student_obj,
                    exam_obj=exam_obj,
                    defaults={'achieve_marks': marks}  # If new, set marks
                )

                # ✅ If marks already exist, update them
                if not created:
                    mark_entry.achieve_marks = marks
                    mark_entry.save()

        return redirect('add_mark')  # Redirect after saving

    return render(request, 'add_mark.html', {
        'classes': classes,
        'students': students,
        'exams': exams,
        'selected_exam': selected_exam,
        'selected_class_id': selected_class_id,
        'selected_exam_id': selected_exam_id
    })


def view_mark(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class_id')  
    selected_exam = request.GET.get('exam_id')  

    exams = []
    students = []
    students_marks = {}

    if selected_class:
        exams = exam_time_table.objects.filter(Class_obj_id=selected_class)  
        students = student.objects.filter(class_obj_id=selected_class)  # Get all students of the selected class

    if selected_exam:
        marks_queryset = Marks.objects.filter(exam_obj_id=selected_exam).select_related('student_obj')
        
        # Store marks in a dictionary with student_id as the key
        students_marks = {mark.student_obj.id: mark for mark in marks_queryset}

    # ✅ Ensure the function always returns an HttpResponse
    return render(request, 'view_mark.html', {
        'classes': classes,
        'exams': exams,
        'students': students,  
        'students_marks': students_marks,  
        'selected_class': selected_class,
        'selected_exam': selected_exam
    })



def update_mark(request,mark_id):
    exam = get_object_or_404(Marks, id=mark_id)
    classes = Class.objects.all()
    subjects = Subjects.objects.filter(class_obj=exam.exam_obj.Class_obj)  # Filter subjects by the selected class
    
    selected_class = exam.exam_obj.Class_obj.id  # Store selected class for persistence
    
    if request.method == 'POST':
        selected_class = request.POST.get('class_id')  # Capture selected class from form
        subjects = Subjects.objects.filter(class_obj=selected_class)  # Filter subjects for that class
        
        # If the update form is submitted
        if 'update_exam' in request.POST:
            exam.exam_obj.exam_name = request.POST.get('exam_name')
            exam.student_obj.name = request.POST.get('date')
            exam.achieve_marks= request.POST.get('time')
            exam.exam_obj.total_marks = request.POST.get('total_marks')
            exam.exam_obj.Class_obj.name = selected_class
            exam.exam_obj.Subjects_obj.sub_name = request.POST.get('subject_id')
            exam.save()
            return redirect('view_mark')

    return render(request, 'update_mark.html', {
        'exam': exam,
        'classes': classes,
        'subjects': subjects,
        'selected_class': selected_class
    })

def delete_mark(request, mark_id):
    Student = get_object_or_404(Marks, id=mark_id)
    if request.method == "POST":
        Student.delete()
        return redirect("view_mark")  # Redirect after deletion

    return render(request, "confirm_delete_mark.html", {"student": Student})
      
# -----------Subject-----------

def add_sub(request):
    clas=Class.objects.all()
    if request.method=='POST':
        class_id = request.POST.get('select')
        subj_name = request.POST.get('subname')
        
        if class_id:
            class_instance = Class.objects.get(id=class_id)
            Subjects.objects.create(class_obj=class_instance,sub_name=subj_name)
            return render(request,'subject_add.html',{'sucessfully':'sucessfully store'})
        else:
            return render(request,'subject_add.html',{'error':'All feild are required! Please enter First'})
    else:
        return render(request,'subject_add.html',{'cls':clas})
    
def view_sub(request):
    selected_class_id = request.GET.get('class_id', None)
    classes = Class.objects.all()
    subjects = Subjects.objects.filter(class_obj_id=selected_class_id) if selected_class_id else None
    return render(request, 'view_sub.html', {
        'classes': classes,
        'subjects': subjects,
        'selected_class_id': selected_class_id
    })

def update_sub(request, sub_id):
    students = get_object_or_404(Subjects, id=sub_id)
    clas=Class.objects.all()

    if request.method == "POST":
        students.sub_name = request.POST.get("name")
        class_id = request.POST.get("class_obj")
        if class_id:
            students.class_obj = get_object_or_404(Class, id=class_id) # Ensure ID is passed
        students.save()
        return redirect("view_sub")  # Redirect to the student list page

    return render(request, "update_sub.html", {"student": students,'classes':clas})

def delete_sub(request,sub_id):
    Student = get_object_or_404(Subjects, id=sub_id)

    if request.method == "POST":
        Student.delete()
        return redirect("view_sub")  # Redirect after deletion

    return render(request, "confirm_delete_subject.html", {"student": Student})

# -------------log out------------

def logout(request):
    del request.session['email']
    return redirect('home')

# ----------batch time table--------

def add_batchtimetable(request):
    classes = Class.objects.all()
    selected_class = request.GET.get('class_id')
    subjects = []
    batches = []
    timetable = {}

    if selected_class:
        # Fetch subjects and batches related to the selected class
        subjects = Subjects.objects.filter(class_obj=selected_class)
        batches = division.objects.filter(class_obj=selected_class)

        # Fetch existing timetable entries for this class
        timetable_entries = batch_time_table.objects.filter(class_obj=selected_class)
        
        # Organize timetable data in a structured dictionary
        for entry in timetable_entries:
            time_slot = f"{entry.time} - {entry.e_time}"  # Example: "12:00 - 1"
            if time_slot not in timetable:
                timetable[time_slot] = { 
                    "Monday": "", "Tuesday": "", "Wednesday": "",
                    "Thursday": "", "Friday": "", "Saturday": "", "Sunday": "" 
                }
            timetable[time_slot][entry.day] = entry.Subjects_obj.sub_name  # Assign subject to correct day

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        batch_id = request.POST.get('batch_id')
        subject_id = request.POST.get('subject_id')
        day = request.POST.get('day')
        time_slot = request.POST.get('time_slot')
        e_time_slot = request.POST.get('e_time_slot')
        print(e_time_slot)
        if class_id and batch_id and subject_id and time_slot and e_time_slot and day:
            class_obj = get_object_or_404(Class, id=class_id)
            batch_obj = get_object_or_404(division, id=batch_id)
            subject_obj = get_object_or_404(Subjects, id=subject_id)
            
           
            batch_time_table.objects.create(
                class_obj=class_obj,
                batch_obj=batch_obj,
                Subjects_obj=subject_obj,
                time=time_slot,
                e_time=e_time_slot,
                day=day
            )
            return render(request, 'add_batch_timetable.html', {
                'successfully': 'Successfully stored!',
                'class': classes,
                'subject': subjects,
                'batches': batches,
                'selected_class': selected_class,
                'timetable': timetable
            })

    return render(request, 'add_batch_timetable.html', {
        'class': classes,
        'subject': subjects,
        'batches': batches,
        'selected_class': selected_class,
        'timetable': timetable
    })   
    
def view_batchtimetable(request):
    selected_class_id = request.GET.get('class_id')
    selected_batch_id = request.GET.get('batch_id')

    # Fetch all classes
    classes = Class.objects.all()

    # Convert `selected_class_id` to int if it exists
    if selected_class_id:
        try:
            selected_class_id = int(selected_class_id)
        except ValueError:
            selected_class_id = None

    # Fetch batches based on selected class
    batches = division.objects.filter(class_obj_id=selected_class_id) if selected_class_id else division.objects.none()

    # Days of the week for table headers
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Fetch timetable entries
    if selected_batch_id:
        try:
            selected_batch_id = int(selected_batch_id)
            timetable_entries = batch_time_table.objects.filter(batch_obj_id=selected_batch_id)
        except ValueError:
            timetable_entries = []
    else:
        timetable_entries = []

    # Structure the timetable by time slot
    structured_timetable = {}
    for entry in timetable_entries:
        time_slot = f"{entry.time} - {entry.e_time}"
        if time_slot not in structured_timetable:
            structured_timetable[time_slot] = {day: "" for day in days_of_week}
        
        structured_timetable[time_slot][entry.day] = entry.Subjects_obj.sub_name

    return render(request, 'view_timetable.html', {
        'classes': classes,
        'batches': batches,
        'timetable_entries':timetable_entries,
        'structured_timetable': structured_timetable,
        'days_of_week': days_of_week,
        'selected_class_id': selected_class_id,
        'selected_batch_id': selected_batch_id,
    }) 



# Update view
def update_bt(request, bt_id):
    timetable_entry = get_object_or_404(batch_time_table, id=bt_id)

    if request.method == 'POST':
        # Directly update the fields without using a form
        timetable_entry.time = request.POST.get('time_slot', timetable_entry.time)
        timetable_entry.Subjects_obj= request.POST.get('subjects', timetable_entry.Subjects_obj)
        timetable_entry.day = request.POST.get('day', timetable_entry.day)
        
        timetable_entry.save()  # Save the updated timetable entry
        
        return redirect('view_timetable')  # Redirect to the timetable view page
    
    return render(request, 'update_timetable.html', {'timetable_entry': timetable_entry})


# Delete view
def delete_bt(request, bt_id):
    timetable_entry = get_object_or_404(batch_time_table, id=bt_id)

    if request.method == 'POST':
        timetable_entry.delete()  # Delete the timetable entry
        return redirect('view_timetable')  # Redirect to the timetable view page

    return render(request, 'delete_timetable.html', {'timetable_entry': timetable_entry})

# --------------------Exam Time Table-----------

def add_examtimetable(request):
    subjects = Subjects.objects.all()  # Fetch all subjects
    classes = Class.objects.all()  # Fetch all classes
    selected_class_id = None
    filtered_subjects = []

    if request.method == 'POST':
        name = request.POST.get('examname')
        day = request.POST.get("day")
        total_marks = request.POST.get('marks')
        date = request.POST.get("date")
        sub_id = request.POST.get('subject_id')
        cls_id = request.POST.get('class_id')
        time_slot = request.POST.get("times")
        e_time_slot = request.POST.get("e_times")

        # If class is selected, filter subjects based on selected class
        if cls_id:
            selected_class_id = cls_id
            filtered_subjects = Subjects.objects.filter(class_obj_id=cls_id)  # Adjust according to your model

        # If form is submitted with all required fields
        if name and time_slot and day and total_marks and date and sub_id and cls_id and e_time_slot:
            Subjects_instance = Subjects.objects.get(id=sub_id)
            class_instance = Class.objects.get(id=cls_id)
            exam_time_table.objects.create(
                Class_obj=class_instance, 
                exam_name=name, 
                day=day, 
                total_marks=total_marks, 
                date=date, 
                Subjects_obj=Subjects_instance, 
                e_time=e_time_slot, 
                time=time_slot
            )
            return render(request, 'add_examtable.html', {'sucessfully': 'Successfully stored', "classes": classes, "subjects": filtered_subjects, "selected_class": selected_class_id})

    return render(request, 'add_examtable.html', {"classes": classes, "subjects": filtered_subjects, "selected_class": selected_class_id})

def view_examtimetable(request):
    selected_class_id = request.GET.get('class_id', None)  # Get selected class
    selected_exam_name = request.GET.get('exam_name', None)  # Get selected exam

    classes = Class.objects.all()  # Get all classes
    exams = []  # List to store exam names for selected class
    timetables = []  # List to store exam timetable details

    if selected_class_id:
        # Get distinct exam names for the selected class
        exams = exam_time_table.objects.filter(Class_obj_id=selected_class_id).values_list('exam_name', flat=True).distinct()
        
        if selected_exam_name:
            # Get the timetable details for the selected exam in the selected class
            timetables = exam_time_table.objects.filter(Class_obj_id=selected_class_id, exam_name=selected_exam_name)

    return render(request, 'viewexam.html', {
        'classes': classes,
        'exams': exams,
        'timetables': timetables,
        'selected_class_id': selected_class_id,
        'selected_exam_name': selected_exam_name
    })



def update_exam(request, exam_id):
    exam = get_object_or_404(exam_time_table, id=exam_id)
    classes = Class.objects.all()
    subjects = Subjects.objects.filter(class_obj=exam.Class_obj)  # Filter subjects by the selected class
    
    selected_class = exam.Class_obj.id  # Store selected class for persistence
    
    if request.method == 'POST':
        selected_class = request.POST.get('class_id')  # Capture selected class from form
        subjects = Subjects.objects.filter(class_obj=selected_class)  # Filter subjects for that class
        
        # If the update form is submitted
        if 'update_exam' in request.POST:
            exam.exam_name = request.POST.get('exam_name')
            exam.date = request.POST.get('date')
            exam.time = request.POST.get('time')
            exam.e_time = request.POST.get('e_time')
            exam.day = request.POST.get('day')
            exam.total_marks = request.POST.get('total_marks')
            exam.Class_obj.name = selected_class
            exam.Subjects_obj.sub_name = request.POST.get('subject_id')
            exam.save()
            return redirect('viewexamtimetable')

    return render(request, 'update_exam.html', {
        'exam': exam,
        'classes': classes,
        'subjects': subjects,
        'selected_class': selected_class
    })

def delete_exam(request, exam_id):
    Student = get_object_or_404(exam_time_table, id=exam_id)
    if request.method == "POST":
        Student.delete()
        return redirect("viewexamtimetable")  # Redirect after deletion

    return render(request, "confirm_delete_exam.html", {"student": Student})

# --------------payment processs-----------------

def payment(request, inquiry_id):
    Inquiry= get_object_or_404(inquiry, id=inquiry_id)
    fee = Fee.objects.get(class_related=Inquiry.class_obj)
    if request.method == "POST":
        order_amount = int(fee.amount* 100)  # Convert to paisa
        order_currency = "INR"
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": order_amount,
            "currency": order_currency,
            "payment_capture": "1"
        })
         
        # Save payment record with Razorpay order ID
        pay.objects.create(
            student_name=Inquiry,
            amount=int(fee.amount* 100),  # Convert back to rupees for display
            razorpay_order_id=razorpay_order['id']
        )

        return render(request, "confirm_payment.html", {
            "order_id": razorpay_order['id'],
            "amount":fee,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "inquiry":Inquiry
        })
    return render(request, "pay.html",{'registration':Inquiry, "fee": fee})


@csrf_exempt
def payment_success(request,inquiry_id):
    inquirys = get_object_or_404(inquiry, id=inquiry_id)
    if request.method == "POST":
        
        data = request.POST
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        # Verify payment signature
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Update payment record
            payment = pay.objects.get(razorpay_order_id=razorpay_order_id)
            
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = True
            payment.save()

            subject = "Student Payment Successful"
            message = f"Student {inquirys.name} (Email: {inquirys.email}) has successfully completed the payment."
            admin_email = "rpatel17381@gmail.com"  # Replace with the actual admin email
            send_mail(subject, message, "no-reply@example.com", [admin_email])

            # Add student to Student table
           
            return render(request, "payment_success.html")
        except razorpay.errors.SignatureVerificationError:
            return render(request, "payment_failed.html")
    return redirect("payment")


def payment_failed(request):
    return render(request, "payment_failed.html")


def admin_view_payment(request):
    selected_class_id = request.GET.get('class_id', None)
    classes = Class.objects.all()
    pays = pay.objects.none()  # Default empty queryset
    if selected_class_id:
       inquiries = inquiry.objects.filter(class_obj=selected_class_id).values_list('id', flat=True)
       pays = pay.objects.filter(student_name_id__in=inquiries)

    return render(request, 'admin_view_payment.html', {
        'class': classes,
        'pay': pays,
        'selected_class_id': selected_class_id
    })

def update_payment(request, payment_id):
    students = get_object_or_404(pay, id=payment_id)
    s=student.objects.all()
    if request.method == "POST":
        students.amount = request.POST.get("amount")
        students.status = request.POST.get("status")
        class_id = request.POST.get("class_obj")
        if class_id:
            students.student_name = get_object_or_404(inquiry, id=class_id) # Ensure ID is passed
        students.save()
        return redirect("admin_payment")  # Redirect to the student list page

    return render(request, "update_payment.html", {"student": students,'classes':s})

def delete_payment(request, payment_id):
    Student = get_object_or_404(pay, id=payment_id)
    if request.method == "POST":
        Student.delete()
        return redirect("admin_payment")  # Redirect after deletion

    return render(request, "confirm_delete_payment.html", {"student": Student})

# ----------------------Attendance---------------------------


def mark_attendance(request):
    classes = Class.objects.all()
    batches = None
    students = None
    selected_class = None
    selected_batch = None
    selected_date = request.POST.get('date', str(date.today()))

    if request.method == "POST":
        selected_class = request.POST.get("class")
        selected_batch = request.POST.get("batch")

        if selected_class:
            batches =division.objects.filter(class_obj_id=selected_class)

        if selected_batch:
            students = student.objects.filter(batch=selected_batch)

        if "submit_attendance" in request.POST:
            for students in students:
                status = request.POST.get(f"attendance_{students.id}", "Absent")
                Attendance.objects.create(student=students, date=selected_date, status=status)
            return redirect("mark_attendance")

    return render(request, "take_attendance.html", {
        "classes": classes,
        "batches": batches,
        "students": students,
        "selected_class": selected_class,
        "selected_batch": selected_batch,
        "selected_date": selected_date,
    })



def batch_wise_attendance(request):
    batches = division.objects.all()  # Fetch all batches
    selected_batch = request.GET.get('batch_id')  # Get selected batch from dropdown
    attendance_records = None  

    if selected_batch:
        students = student.objects.filter(batch=selected_batch)  # Get students in batch
        attendance_records = Attendance.objects.filter(student__in=students).order_by('-date')

    return render(request, 'batch_wise_attendance.html', {
        'batches': batches,
        'attendance_records': attendance_records,
        'selected_batch': selected_batch
    })

def admin_update_attendance(request, attendance_id):
    attendance_record = get_object_or_404(Attendance, id=attendance_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        attendance_record.status = new_status
        attendance_record.save()
        return redirect("batch_wise_attendance")  # Redirect back to list

    return render(request, "admin_update_attendance.html", {"attendance": attendance_record})

def admin_delete_attendance(request, attendance_id):
    Student = get_object_or_404(Attendance, id=attendance_id)
    if request.method == "POST":
        Student.delete()
        return redirect("admin_payment")  # Redirect after deletion

    return render(request, "confirm_delete_attendance.html", {"student": Student})
 # Redirect after deletion

# -------------quiz-----------------------

# ✅ Get logged-in teacher from session
def get_logged_in_teacher(request):
    if 'email' in request.session:
        return approveteacher.objects.filter(email=request.session['email']).first()
    return None

# ✅ Create Quiz View
  # Redirect if not logged in
def create_quiz(request):
    if 'email' not in request.session:
        return redirect('login')  # Ensure user is logged in

    # Get the logged-in teacher object
    teacher = get_object_or_404(approveteacher, email=request.session['email'])

    # Get all approved classes for this teacher
    approved_classes = approveteacher.objects.filter(email=request.session['email'])

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        class_id = request.POST.get("class", "").strip()
        subject_id = request.POST.get("subject", "").strip()

        print("Received Data:", title, class_id, subject_id)  # Debugging

        # Check if any field is empty
        if not title or not class_id or not subject_id:
            return render(request, "create_quiz.html", {
                "approved_classes": approved_classes,
                "error": "All fields are required!",
            })

        try:
            class_obj = get_object_or_404(Class, id=int(class_id))
            subject_obj = get_object_or_404(Subjects, id=int(subject_id))
        except ValueError:
            return render(request, "create_quiz.html", {
                "approved_classes": approved_classes,
                "error": "Invalid class or subject selection!",
            })

        # Ensure teacher is allowed to create a quiz for the selected class & subject
        if not approveteacher.objects.filter(email=teacher.email, Class_obj=class_obj, Subjects=subject_obj).exists():
            return render(request, "create_quiz.html", {
                "approved_classes": approved_classes,
                "error": "You are not allowed to create a quiz for this class/subject!",
            })

        # ✅ Create Quiz
        quiz = Quiz.objects.create(
            teacher=teacher,  # Fix: Get teacher object
            class_obj=class_obj,
            subject_obj=subject_obj,
            title=title
        )

        return redirect("add_questions", quiz_id=quiz.id)  # Redirect to add questions

    return render(request, "create_quiz.html", {"approved_classes": approved_classes})

# ✅ Add Questions to Quiz
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        text = request.POST.get("question")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        correct_option = request.POST.get("correct_option")
        marks = request.POST.get("marks")

        if not text or not option1 or not option2 or not option3 or not option4 or not correct_option or not marks:
            return render(request, "que.html", {
                "quiz": quiz,
                "error": "All fields are required!",
            })

        try:
            marks = int(marks)
        except ValueError:
            return render(request, "add_questions.html", {
                "quiz": quiz,
                "error": "Marks must be a number!",
            })

        Questions_Ans.objects.create(
            quiz=quiz,
            text=text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            marks=marks
        )

        # ✅ Update total marks
        quiz.total_marks = Questions_Ans.objects.filter(quiz=quiz).aggregate(Sum('marks'))['marks__sum'] or 0
        quiz.save()

        return redirect("add_questions", quiz_id=quiz.id)

    return render(request, "que.html", {"quiz": quiz})




# ✅ Get logged-in student from session
def get_logged_in_student(request):
    if 'email' in request.session:
        return student.objects.filter(email=request.session['email']).first()
    return None

# ✅ View Available Quizzes (Only for Student's Class)
def student_view_quizzes(request):
    student_obj = get_logged_in_student(request)
    if not student_obj:
        return redirect('login')

    quizzes = Quiz.objects.filter(class_obj=student_obj.class_obj)  # Only quizzes for student's class
    return render(request, "student_quizzes.html", {"quizzes": quizzes})

# ✅ Attempt Quiz
def attempt_quiz(request, quiz_id):
    student_obj = get_logged_in_student(request)
    if not student_obj:
        return redirect('login')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Questions_Ans.objects.filter(quiz=quiz)

    # ✅ Prevent Multiple Attempts
    existing_attempt = StudentQuiz.objects.filter(student=student_obj, quiz=quiz).first()
    if existing_attempt:
        return render(request, "quiz_already_attempted.html", {"quiz": quiz, "marks": existing_attempt.achieved_marks})

    if request.method == "POST":
        achieved_marks = 0

        for question in questions:
            selected_option = request.POST.get(f"question_{question.id}")

            if selected_option and selected_option == question.correct_option:
                achieved_marks += question.marks  # ✅ Add marks for correct answers

        # ✅ Save Student's Attempt (Only Once)
        StudentQuiz.objects.create(
            student=student_obj,
            quiz=quiz,
            achieved_marks=achieved_marks
        )

        return redirect("view_quiz_marks")

    return render(request, "student_view_quiz.html", {"quiz": quiz, "questions": questions})

# ✅ View Quiz Marks
def view_quiz_marks(request):
    student_obj = get_logged_in_student(request)
    if not student_obj:
        return redirect('login')

    marks = StudentQuiz.objects.filter(student=student_obj)
    return render(request, "quiz_mark.html", {"marks": marks})

def view_quizzes(request):
    if 'email' not in request.session:
        return redirect('login')  # Ensure user is logged in

    teacher = get_object_or_404(approveteacher, email=request.session['email'])
    quizzes = Quiz.objects.filter(teacher=teacher)  # Get only quizzes created by this teacher

    return render(request, "view_quizzes.html", {"quizzes": quizzes})



def delete_quiz(request, quiz_id):
    if 'email' not in request.session:
        return redirect('login')  # Ensure user is logged in

    teacher = get_object_or_404(approveteacher, email=request.session['email'])
    quiz = get_object_or_404(Quiz, id=quiz_id, teacher=teacher)  # Ensure only the owner can delete

    if request.method == "POST":
        quiz.delete()
        return redirect('teacher_view_quizzes')  # Redirect to the quiz list

    return render(request, "delete_quiz.html", {"quiz": quiz})

def update_quiz(request, quiz_id):
    if 'email' not in request.session:
        return redirect('login')

    teacher = get_object_or_404(approveteacher, email=request.session['email'])
    quiz = get_object_or_404(Quiz, id=quiz_id, teacher=teacher)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if not title:
            return render(request, "update_quiz.html", {"quiz": quiz, "error": "Title is required!"})
        
        quiz.title = title
        quiz.save()
        return redirect('teacher_view_quizzes')

    return render(request, "update_quiz.html", {"quiz": quiz})


from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

  # Replace with your actual Student model

def student_forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        students = student.objects.filter(email=email).first()  # Check if email exists in Student table
        
        if student:
            token = get_random_string(50)  # Generate reset token
            students.reset_token = token  # Save token in DB
            students.save()

            reset_link = request.build_absolute_uri(f"/student-reset-password/{token}/")
            send_mail(
                "Password Reset Request",
                f"Click here to reset your password: {reset_link}",
                "admin@example.com",  # Change to your email
                [email],
                fail_silently=False,
            )
            return render(request, "student_forgot_password.html", {"message": "Reset link sent to your email!"})
        else:
            return render(request, "student_forgot_password.html", {"message": "Email not found!"})
    
    return render(request, "student_forgot_password.html")


def student_reset_password(request, token):
    students = student.objects.filter(reset_token=token).first()
    
    if not students:
        return render(request, "student_reset_password.html", {"message": "Invalid or expired link!"})

    if request.method == "POST":
        new_password = request.POST["password"]
        cnew_password = request.POST["cpassword"]
        if new_password==cnew_password:
            students.pas = new_password  # Hash the password
            students.save()
            return render(request, "student_reset_password.html", {"message": "Password reset successful! You can now login."})
        else:
           return render(request, "student_reset_password.html", {"error": "Both Password Are Not Same"})

    return render(request, "student_reset_password.html")

def teacher_forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        students = approveteacher.objects.filter(email=email).first()  # Check if email exists in Student table
        
        if student:
            token = get_random_string(50)  # Generate reset token
            students.reset_token = token  # Save token in DB
            students.save()

            reset_link = request.build_absolute_uri(f"/teacher-reset-password/{token}/")
            send_mail(
                "Password Reset Request",
                f"Click here to reset your password: {reset_link}",
                "admin@example.com",  # Change to your email
                [email],
                fail_silently=False,
            )
            return render(request, "teacher_forgot_password.html", {"message": "Reset link sent to your email!"})
        else:
            return render(request, "teacher_forgot_password.html", {"message": "Email not found!"})
    
    return render(request, "teacher_forgot_password.html")


def teacher_reset_password(request, token):
    students = approveteacher.objects.filter(reset_token=token).first()
    
    if not students:
        return render(request, "teacher_reset_password.html", {"message": "Invalid or expired link!"})

    if request.method == "POST":
        new_password = request.POST["password"]
        students.pas = new_password  # Hash the password
        cnew_password = request.POST["cpassword"]
        if new_password==cnew_password:
            students.pas = new_password  # Hash the password
            students.save()
            return render(request, "teacher_reset_password.html", {"message": "Password reset successful! You can now login."})
        else:
           return render(request, "teacher_reset_password.html", {"error": "Both Password Are Not Same"})
    return render(request, "teacher_reset_password.html")

def staff_forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        students = approvestaff.objects.filter(email=email).first()  # Check if email exists in Student table
        
        if student:
            token = get_random_string(50)  # Generate reset token
            students.reset_token = token  # Save token in DB
            students.save()

            reset_link = request.build_absolute_uri(f"/staff-reset-password/{token}/")
            send_mail(
                "Password Reset Request",
                f"Click here to reset your password: {reset_link}",
                "admin@example.com",  # Change to your email
                [email],
                fail_silently=False,
            )
            return render(request, "staff_forgot_password.html", {"message": "Reset link sent to your email!"})
        else:
            return render(request, "staff_forgot_password.html", {"message": "Email not found!"})
    
    return render(request, "staff_forgot_password.html")


def staff_reset_password(request, token):
    students = approvestaff.objects.filter(reset_token=token).first()
    
    if not students:
        return render(request, "staff_reset_password.html", {"message": "Invalid or expired link!"})

    if request.method == "POST":
        new_password = request.POST["password"]
        students.pas = new_password  # Hash the password
        cnew_password = request.POST["cpassword"]
        if new_password==cnew_password:
            students.pas = new_password  # Hash the password
            students.save()
            return render(request, "staff_reset_password.html", {"message": "Password reset successful! You can now login."})
        else:
           return render(request, "staff_reset_password.html", {"error": "Both Password Are Not Same"})
    return render(request, "staff_reset_password.html")


import csv



def generate_csv_report(request, class_id):
    marks = Marks.objects.filter(exam_obj__Class_obj_id=class_id)  # Filtering by class

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="marks_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Student Email", "Exam Name", "Subject", "Marks Obtained"])  # Updated headers

    for mark in marks:
        writer.writerow([
            mark.student_obj.email,          # Fetching student email
            mark.exam_obj.exam_name,         # Fetching exam name
            mark.exam_obj.Subjects_obj.sub_name, # Fetching subject name from exam timetable
            mark.achieve_marks               # Fetching obtained marks
        ])

    return response



def location_view(request):
    states = State.objects.all()
    cities = []
    areas = []

    selected_state = request.GET.get('state_id')
    selected_city = request.GET.get('city_id')

    if selected_state:
        cities = City.objects.filter(state_id=selected_state)

    if selected_city:
        areas = Area.objects.filter(city_id=selected_city)

    return render(request, 'location.html', {
        'states': states,
        'cities': cities,
        'areas': areas,
        'selected_state': selected_state,
        'selected_city': selected_city
    })

from django.shortcuts import render, redirect
from .models import State, City, Area

# State Insert View
def add_state(request):
    if request.method == "POST":
        name = request.POST.get('state_name')
        if name:
            State.objects.create(name=name)
    return render(request, 'state.html')

# City Insert View
def add_city(request):
    states = State.objects.all()
    if request.method == "POST":
        name = request.POST.get('city_name')
        state_id = request.POST.get('state_id')
        if name and state_id:
            state = State.objects.get(id=state_id)
            City.objects.create(name=name, state=state)
    return render(request, 'city.html', {'states': states})

# Area Insert View
def add_area(request):
    cities = City.objects.all()
    if request.method == "POST":
        name = request.POST.get('area_name')
        city_id = request.POST.get('city_id')
        if name and city_id:
            city = City.objects.get(id=city_id)
            Area.objects.create(name=name, city=city)
    return render(request, 'area.html', {'cities': cities})

# View All Locations
def view_locations(request):
    states = State.objects.all()
    cities = City.objects.all()
    areas = Area.objects.all()
    return render(request, 'location.html', {'states': states, 'cities': cities, 'areas': areas})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from reportlab.platypus import Table, TableStyle # type: ignore
from reportlab.lib import colors # type: ignore
import os
from datetime import datetime
from django.db.models import Count




def generate_report(request):
    classes = Class.objects.all()
    batches = division.objects.all()
    exams = exam_time_table.objects.all()
    return render(request, "generate_report.html", {
        "classes": classes,
        "batches": batches,
        "exams": exams
    })

def process_report(request):
    report_type = request.GET.get("report_type")
    class_id = request.GET.get("class_id")
    batch_id = request.GET.get("batch_id")
    exam_id = request.GET.get("exam_id")
    month = request.GET.get("month")
    year = request.GET.get("year")

    if report_type == "attendance":
        return generate_attendance_pdf(request, year, month, class_id)
    elif report_type == "marks":
        return generate_marks_pdf(request, class_id, exam_id)
    elif report_type == "payment":
        return generate_payment_pdf(request, class_id)
    else:
        return HttpResponse("Invalid Report Type", status=400)



def generate_pdf(response, title, table_data, class_name=None, exam_name=None, report_type=None):
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle(title)

    logo_path = os.path.join(settings.BASE_DIR, 'education/static/img/about.png')

    # **Draw Border**
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(2)
    pdf.rect(30, 690, 540, 90)

    # **Insert Logo**
    if os.path.exists(logo_path):
        pdf.drawImage(logo_path, 40, 700, width=80, height=70)

    # **Header: School Name & Address**
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(180, 750, "PERFECT GROUP TUITION")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(250, 730, "GUJARATI MEDIUM")
    pdf.drawString(140, 710, "A-25, 80 Feet Road, Patanjali Society, Nikol, Ahmedabad")

    # **Dynamic Report Title**
    pdf.setFont("Helvetica-Bold", 14)
    report_title = title.upper()
    
    if report_type == "attendance":
        report_title += f" - {class_name}"
    elif report_type == "marks":
        report_title += f" - {class_name} ({exam_name})"
    elif report_type == "payment":
        report_title += f" - {class_name}"

    pdf.drawString(180, 660, report_title)

    # **Date & Year at the Bottom**
    year = datetime.now().year
    date = datetime.now().strftime("%B %d, %Y") 
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 640, f"Year: {year}")
    pdf.drawString(400, 640, f"Date: {date}")

    # **Generate Table**
    table = Table(table_data, colWidths=[100, 150, 70, 70, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(pdf, 400, 300)
    table.drawOn(pdf, 90, 500)

    # **Footer**
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(250, 100, "THIS IS AN OFFICIAL REPORT")

    pdf.save()
    return response



def generate_attendance_pdf(request, year, month, class_id):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="attendance_report.pdf"'

    # **Fetch attendance & Count Present Days**
    attendance_records = Attendance.objects.filter(
        date__year=year, date__month=month,
        student__class_obj_id=class_id
    ).values('student__roll_no', 'student__name').annotate(present_days=Count('id'))

    table_data = [["Roll No", "Name", "Present Days"]]
    for att in attendance_records:
        table_data.append([
            att["student__roll_no"],
            att["student__name"],
            att["present_days"]
        ])

    class_name = Class.objects.get(id=class_id).name
    return generate_pdf(response, f"Attendance Report - ", table_data, class_name=class_name, report_type="attendance")


def generate_marks_pdf(request, class_id, exam_id):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="marks_report.pdf"'

    # **Fetch Marks Data**
    marks = Marks.objects.filter(exam_obj_id=exam_id, student_obj__class_obj_id=class_id)
    
    table_data = [["Roll No", "Name", "Exam", "Total Marks", "Achieved Marks"]]
    for mark in marks:
        table_data.append([
            mark.student_obj.roll_no,
            mark.student_obj.name,
            mark.exam_obj.exam_name,
            mark.exam_obj.total_marks,
            mark.achieve_marks
        ])

    class_name = Class.objects.get(id=class_id).name
    exam_name = exam_time_table.objects.get(id=exam_id).exam_name
    return generate_pdf(response, f"Marks Report -", table_data, class_name=class_name, exam_name=exam_name, report_type="marks")


def generate_payment_pdf(request, class_id):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="payment_report.pdf"'

    # **Fetch Payment Data**
    payments = pay.objects.filter(student_name__class_obj_id=class_id)

    table_data = [["Status", "Student Name", "Amount"]]
    for payment in payments:
        table_data.append([
            payment.status,
            payment.student_name.name,
            payment.amount
        ])

    class_name = Class.objects.get(id=class_id).name
    return generate_pdf(response, f"Payment Report - ", table_data, class_name=class_name, report_type="payment")




def generate_fee_receipt(request):
    # **Check if Student is Logged In**
    if "email" not in request.session:
        return HttpResponse("Unauthorized", status=401)

    # **Get the Logged-in Student**
    student_email = request.session["email"]
    payment = pay.objects.filter(student_name__email=student_email, status=True).first()

    if not payment:
        return HttpResponse("No payment record found.", status=404)

    # **Create PDF Response**
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="fee_receipt_{payment.student_name.name}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Fee Receipt")

    # **Draw Border**
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(2)
    pdf.rect(50, 40, 500, 700)  # (x, y, width, height)

    # **Institute Header**
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 720, "PERFECT GROUP TUITION")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(250, 700, "GUJARATI MEDIUM")
    pdf.drawString(140, 680, "A-25, 80 Feet Road, Khodiyar Nagar, Nikol, Ahmedabad")
    
    # **Logo (Optional)**
    logo_path = os.path.join(settings.BASE_DIR, 'education/static/img/about.png')
    if os.path.exists(logo_path):
        pdf.drawImage(logo_path, 60, 710, width=80, height=60)

    # **Receipt Title Box**
    pdf.setLineWidth(1)
    # pdf.rect(180, 640, 220, 30)  # Box around "Fee Receipt"
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(250, 650, "FEE RECEIPT")

    # **Student & Payment Details**
    pdf.setFont("Helvetica", 12)
    pdf.drawString(200, 560, f"Student Name: {payment.student_name.name}")
    pdf.drawString(200, 540, f"Payment Date: {datetime.now().strftime('%d-%m-%Y')}")
    pdf.drawString(200, 520, f"Amount Paid: ₹{payment.amount}")

    # **Stamp Section**
   # **Stamp Box (Below the Logo)**
    pdf.setLineWidth(2)
    pdf.rect(100, 120, 130, 130)  # Box for stamp

# **Insert Stamp Image**
    stamp_path = os.path.join(settings.BASE_DIR, 'education/static/img/stamp.png.jpg')  # Adjust path as needed
    if os.path.exists(stamp_path):
       pdf.drawImage(stamp_path, 105, 125, width=120, height=120)  # Fit inside the box
    else:
       pdf.setFont("Helvetica-Bold", 12)
       pdf.drawString(130, 180, "OFFICIAL STAMP")  # Text as fallback

    

    # **Authorized Signature**
    pdf.setLineWidth(1.5)
    pdf.rect(360, 120, 150, 50)  # Box for signature
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(390, 145, "Rajesh Dholariya")  # Signature Name
    pdf.setFont("Helvetica", 10)
    pdf.drawString(390, 130, "Authorized Signatory")

    pdf.save()
    return response

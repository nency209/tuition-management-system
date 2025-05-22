from django.db import models  
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='areas')

    def __str__(self):
        return self.name

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    pas=models.CharField(max_length=15,default='')

    def __str__(self):
        return self.name
# -----------------------
class Class(models.Model):
    name = models.CharField(max_length=50,blank=True)
    def _str_(self):
        return self.name

class Fee(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2,default="",null=False)
    class_related = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="fee",default="")

class inquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),]
    
    name=models.CharField(max_length=10)
    email=models.EmailField()
    mob=models.CharField(max_length=10)
    pmob=models.CharField(max_length=10) 
    bod=models.DateField(auto_now=True)
    add=models.TextField(default="")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='inquiry',default="")
    pas=models.CharField(max_length=50,default="")
    gender=models.CharField(max_length=10,default="") 
    state=models.ForeignKey(State, on_delete=models.CASCADE, related_name='inquiry',default="")
    city=models.ForeignKey(City, on_delete=models.CASCADE, related_name='inquiry',default="")
    area=models.ForeignKey(Area, on_delete=models.CASCADE, related_name='inquiry',default="")
    code=models.CharField(max_length=10,default="")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    image=models.ImageField(upload_to='Pictures\\mom\\',default="")
   
class division(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='batches')
    name = models.CharField(max_length=50,unique=True)

    def _str_(self):
        return self.name
   
class Subjects(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    sub_name = models.CharField(max_length=50)

    def _str_(self):
        return self.name

class pay(models.Model):
    student_name = models.ForeignKey(inquiry, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255,default="")
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=False) 
    amount = models.IntegerField(default='')

class student(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('send', 'send'),
        ]
    
    name=models.CharField(max_length=10)
    email=models.EmailField()
    mob=models.CharField(max_length=10)
    pmob=models.CharField(max_length=10) 
    bod=models.DateField(auto_now=True)
    add=models.TextField(default="")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='student',default="")
    pas=models.CharField(max_length=50,default="")
    gender=models.CharField(max_length=10,default="") 
    pas=models.CharField(max_length=50,default="")
    amount = models.IntegerField(default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    roll_no = models.PositiveIntegerField(null=True, blank=True) 
    batch = models.ForeignKey(division, on_delete=models.SET_NULL, null=True, blank=True)
    reset_token = models.CharField(max_length=50, null=True, blank=True) 
    image=models.ImageField(upload_to='Pictures\\mom\\',default="")
    
@receiver(pre_save, sender=student)
def assign_roll_number_and_batch(sender, instance, **kwargs):
    """
    Auto-assigns roll numbers and batches when a student is added or their class is updated.
    - If class is updated, reassign roll number & batch based on the new class.
    - Maintains sequential order for roll numbers in both old and new classes.
    """

    if instance.pk:  # Check if the student already exists (update case)
        old_instance = student.objects.get(pk=instance.pk)

        if old_instance.class_obj != instance.class_obj:  # Class has been changed
            # Reorder old class (previous class)
            reorder_roll_numbers(old_instance.class_obj)

            # Assign new roll number in the updated class
            instance.roll_no = get_next_roll_number(instance.class_obj)

            # Assign new batch dynamically based on new class
            instance.batch = get_batch_for_student(instance.class_obj, instance.roll_no)

            # Reorder roll numbers in the new class
            reorder_roll_numbers(instance.class_obj)
            return  # No need for further changes, as it's already reassigned

    # If new student is added
    if instance.roll_no is None:
        instance.roll_no = get_next_roll_number(instance.class_obj)

    if instance.batch is None:
        instance.batch = get_batch_for_student(instance.class_obj, instance.roll_no)


def get_next_roll_number(class_obj):
    """
    Returns the next available roll number for a given class.
    """
    last_student = student.objects.filter(class_obj=class_obj).order_by('-roll_no').first()
    return last_student.roll_no + 1 if last_student else 1


def get_batch_for_student(class_obj, roll_no):
    """
    Returns the appropriate batch for a student based on their roll number.
    - First batch (e.g., 'A') for first 10 students.
    - Second batch (e.g., 'B') for students above roll number 10.
    """
    batches = division.objects.filter(class_obj=class_obj).order_by("name")
    if batches.exists():
        return batches.first() if roll_no <= 10 else batches.last()
    return None


def reorder_roll_numbers(class_obj):
    """
    Reassigns roll numbers sequentially to ensure proper order after a student moves classes.
    """
    students = student.objects.filter(class_obj=class_obj).order_by("roll_no")
    for index, student_obj in enumerate(students, start=1):
        student_obj.roll_no = index
        student_obj.batch = get_batch_for_student(class_obj, index)  # Update batch
        student_obj.save(update_fields=["roll_no", "batch"])

class teacher(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approve', 'approve'),
        ]
    name=models.CharField(max_length=10)
    email=models.EmailField()
    mob=models.CharField(max_length=10)
    gender=models.CharField(max_length=10,default="") 
    add=models.TextField(default="")
    pas=models.CharField(max_length=50,default="")
    qulification=models.CharField(max_length=10,default="")
    specialization=models.CharField(max_length=20,default="")
    experience=models.IntegerField()
    Subjects_obj = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='teacher',default='')
    Class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='teacher',null=True,blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    image=models.ImageField(upload_to='Pictures\\mom\\',default="")

class approveteacher(models.Model):
    name=models.CharField(max_length=10)
    email=models.EmailField()
    mob=models.CharField(max_length=10)
    bod=models.DateField(auto_now_add=True)
    gender=models.CharField(max_length=10,default="") 
    add=models.TextField(default="")
    pas=models.CharField(max_length=50,default="")
    qulification=models.CharField(max_length=10,default="")
    specialization=models.CharField(max_length=20,default="")
    experience=models.IntegerField()
    Class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='ateacher',default=0)
    Subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='teacherapprove',default='')
    reset_token = models.CharField(max_length=50, null=True, blank=True) 
    image=models.ImageField(upload_to='Pictures\\mom\\',default="")

class staff(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approve', 'approve'),
        ]
    name=models.CharField(max_length=10)
    email=models.EmailField()
    mob=models.CharField(max_length=10)
    
    gender=models.CharField(max_length=10,default="") 
    pas=models.CharField(max_length=50,default="")
    add=models.TextField(default="")
    qulification=models.CharField(max_length=10,default="")
    specialization=models.CharField(max_length=20,default="")
    experience=models.IntegerField()
    image=models.ImageField(upload_to='Pictures\\mom\\',default="")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


  
class approvestaff(models.Model):
    name=models.CharField(max_length=10)
    email=models.EmailField()
    mob=models.CharField(max_length=10)
    bod=models.DateField(auto_now=True)
    gender=models.CharField(max_length=10,default="") 
    add=models.TextField(default="")
    pas=models.CharField(max_length=50,default="")
    qulification=models.CharField(max_length=10,default="")
    specialization=models.CharField(max_length=20,default="")
    experience=models.IntegerField()
    reset_token = models.CharField(max_length=50, null=True, blank=True) 
    image=models.ImageField(upload_to='Pictures\\mom\\',default="")

class gallery(models.Model):
    image=models.ImageField(upload_to='Pictures\\mom\\')
    year=models.IntegerField(default="")

class notice(models.Model):
    date=models.DateField(auto_now_add=True)
    name=models.CharField(max_length=10)
    msg=models.CharField(max_length=500)



class batch_time_table(models.Model):
    DAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    time = models.TimeField()
    e_time=models.TimeField()
    day=models.CharField(max_length=10, choices=DAYS)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='batchtimetable')
    batch_obj = models.ForeignKey(division, on_delete=models.CASCADE, related_name='batchtimetable')
    Subjects_obj = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='batchtimetable')


class exam_time_table(models.Model):
    exam_name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    e_time=models.TimeField()
    day = models.CharField(max_length=10)
    total_marks = models.IntegerField()
    Subjects_obj = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='examtimetable')
    Class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='examtimetable',default=0)
    

class Marks(models.Model):
    achieve_marks = models.IntegerField()
    student_obj= models.ForeignKey(student, on_delete=models.CASCADE,default='')
    exam_obj = models.ForeignKey(exam_time_table, on_delete=models.CASCADE,related_name='marks')


class Study_Material(models.Model):
    teacher_obj = models.ForeignKey(approveteacher, on_delete=models.CASCADE,related_name='study_material')
    pdf_url=models.FileField(upload_to='documents/',default='')
    date = models.DateField(auto_now_add=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sm',default="")
    

class Tuition(models.Model):
    tuition_name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    location_url = models.CharField(max_length=100)
    contact_no = models.BigIntegerField()
    pin_code = models.IntegerField()

class Attendance(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE,default='')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])


class Quiz(models.Model):
    teacher = models.ForeignKey("ApproveTeacher", on_delete=models.CASCADE)  # ✅ No default=''
    class_obj = models.ForeignKey("Class", on_delete=models.CASCADE)  # ✅ No default=''
    subject_obj = models.ForeignKey("Subjects", on_delete=models.CASCADE)  # ✅ No default=''
    title = models.CharField(max_length=200, default='')
    total_marks = models.IntegerField(default=0)

    class Meta:
        unique_together = ('teacher', 'title') 

    def __str__(self):
        return f"{self.title} ({self.class_obj.name} - {self.subject_obj.name})"

class Questions_Ans(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # ✅ No default=''
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    marks = models.IntegerField()

    def __str__(self):
        return self.text

class StudentQuiz(models.Model):
    student = models.ForeignKey("student", on_delete=models.CASCADE)  # ✅ No default=''
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # ✅ No default=''
    achieved_marks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.email} - {self.quiz.title} ({self.achieved_marks} Marks)"
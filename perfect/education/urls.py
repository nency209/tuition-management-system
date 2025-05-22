from django.urls import path,include
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('',home,name='home'),

    # -------------------------admin----------------------
   
    path('admin1/add-state/', add_state, name='add_state'),
    path('admin1/add-city/', add_city, name='add_city'),
    path('admin1/add-area/', add_area, name='add_area'),
    path('admin1/view-locations/', view_locations, name='view_locations'),
    path(' admin_profile/', admin_profile,name=' admin_profile'),
    path('admin1/',admin_dashboard,name='admin_dashboard'),
    path('adminmanage/',adminmanage,name='admin_manage'),
    path('admin_view_mark/',admin_view_mark,name='admin_view_mark'),
    path('admin_view_batch_wise_attendance/',admin_view_batch_wise_attendance,name='admin_view_batch_wise_attendance'),
    path('adminLogin/',adminlogin,name='adminlogin'),
    path("admin-dashboard/", admin_dashboard2, name="admin_dashboard"),

    # ----------------- static fee --------------------

    path('adminfee/',admin_fee,name='admin_fee'),
    path('manage_fee_detail/',view_fee_detail,name='view_fee_detail'),
    path('adminviewfee/',admin_view_payment,name='admin_view_payment'),
    path('fee/update/<int:fee_id>/', update_fee, name='update_fee'),
    path('fee/delete/<int:fee_id>/', delete_fee, name='delete_fee'),
    
    
    #------------------------- teacher------------------------

    path('admin_teacher/',admin_teacher,name='admin_teacher'),
    path('teacherview/',viewteacher,name='view_teacher'),
    path('tp/',teacherpersonal,name='tp'),
    path('teacher',teacher_dashboard,name='teacher_dashboard'),
    path('tutorLogin/',Logintutor,name='Logintutor'),
    path('approve_teacher/<int:teacher_id>/', approve_teacher,name='approve_teacher'),
    path('teacher_profile/', teacher_profile,name='teacher_profile'),
    path('tutor/', tutor,name='tutor'),
    path('approvet_teacher_detail/', approvet_teacher_detail,name='approvet_teacher_detail'),
    path('teacher/update/<int:teacher_id>/', update_teacher, name='update_teacher'),
    path('teacher/delete/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('iteacher/delete/<int:iteacher_id>/', delete_iteacher, name='delete_iteacher'),
    path('teacher_view_exam/', teacher_view_exam,name='teacher_view_exam'),
    path('teacher_batch_timetable/',teacher_batch_timetable,name='teacher_batch_timetable'),
     path('teacher_view_quizzes/',teacher_view_quizzes,name='teacher_view_quizzes'),
    # --------------------staff---------------------------

    path('staffview/',viewstaff,name='view_staff'),
    path('admin_staff/',admin_staff,name='admin_staff'),
    path('sp/',Staffpersonal,name='sp'),
    path('staff',staff_dashboard,name='staff_dashboard'),
    path('Loginstaff/',Loginstaff,name='Loginstaff'),
    path('approve_staff/<int:staff_id>/',approve_staff,name='approve_staff'),
    path('staff_profile/', staff_profile,name='staff_profile'),
    path('staff_details/',staff_details,name='staff_details'),
    path('approvet_staff_detail/', approvet_staff_detail,name='approvet_staff_detail'),
    path('staff/update/<int:staff_id>/', update_staff, name='update_staff'),
    path('staff/delete/<int:staff_id>/', delete_staff, name='delete_staff'),
    path('istaff/delete/<int:istaff_id>/', delete_istaff, name='delete_istaff'),

    # --------------------------student-----------------------

    path('admin_student/',admin_student,name='admin_student'),
    path("approve/<int:inquiry_id>/", approve_student, name="approve_student"),
    path('studentview/',inquirystudent,name='admin_view__student'),
    path('admission/',Inquiry,name='admissionpage'),
    path('studentes',student_dashboard,name='student_dashboard'),
    path("check-payment/", pay_student, name="pay_student"),
    path("view-stu/", paystudent, name="viewpay_student"),
    path("sendlogin/<int:student_id>/", send_studentlogin, name="send_studentlogin"),
    path('Login/',Login,name='Login'),
    path('profile/',student_profile,name='student_profile'),
    path('student_timetable/',student_timetable,name='student_timetable'),
    path('student_studymaterial/',student_studymaterial,name='student_studymaterial'),
    path('student/update/<int:student_id>/', update_student, name='update_student'),
    path('student/delete/<int:student_id>/', delete_student, name='delete_student'),
    path('student1/delete/<int:istudent_id>/',delete_istudent,name='delete_istudent'),
    path('student_examtimetable',student_examtimetable,name="student_examtimetable"),
    path('student_mark',student_mark,name="student_mark"),

    #---------------------- batch----------------

    path('add_batch',add_batch,name='batch_add'),
    path('view_batch',view_batch,name='batch_view'),
    path('batch/update/<int:batch_id>/', update_batch, name='update_batch'),
    path('batch/delete/<int:batch_id>/', delete_batch, name='delete_batch'),

    # ------------------class-------------

    path('add_class',add_class,name='class_add'),
    path('view_class',view_class,name='class_view'),
    path('class/update/<int:class_id>/', update_class, name='update_class'),
    path('class/delete/<int:class_id>/', delete_class, name='delete_class'),

    # -----------------------subject----------------

    path('add_sub',add_sub,name='add_sub'),
    path('view_sub',view_sub,name='view_sub'),
    path('sub/update/<int:sub_id>/', update_sub, name='update_sub'),
    path('sub/delete/<int:sub_id>/', delete_sub, name='delete_sub'),

    
    # --------------------notice------------------

    path('notice/',notices,name='notice'),
    path("notices/", view_notices, name="view_notices"),
    path("anotices/", aview_notices, name="aview_notices"),
    path('n/delete/<int:notice_id>/', delete_notice, name='delete_notice'),

    # -------------------------gallery-------------

    path('add_gallery',add_gallery,name='add_gallery'),
    path('view_gallery',view_gallery,name='view_gallery'),
    path('g/update/<int:gallery_id>/', update_gallery, name='update_gallery'),
    path('g/delete/<int:gallery_id>/', delete_gallery, name='delete_gallery'),
    #---------------------------- Study Material-------------

    path('add_sm',add_sm,name='add_sm'),
     path('view_sm',view_sm,name='view_sm'),
    path('sm/update/<int:sm_id>/', update_sm, name='update_sm'),
    path('sm/delete/<int:sm_id>/', delete_sm, name='delete_sm'),
     
    # ---------------------Mark------------------------

    path('add_mark',add_mark,name='add_mark'),
    path('view_mark',view_mark,name='view_mark'),
    path('mark/update/<int:mark_id>/', update_mark, name='update_mark'),
    path('mark/delete/<int:mark_id>/', delete_mark, name='delete_mark'),

    # ------------------logout------------

    path('logout',logout,name="logout"),

    # ------------------batch time table----------------

    path('addbatchtimetable',add_batchtimetable,name="addbatchtimetable"),
    path('viewbatchtimetable',view_batchtimetable,name="viewbatchtimetable"),
    path('update/<int:batch_time_table_id>/', update_bt, name='update_bt'),
    path('delete/<int:bt_id>/', delete_bt, name='delete_bt'),

   # -------------------exam time table------------------------

    path('addexamtimetable',add_examtimetable,name="addexamtimetable"),
    path('viewexamtimetable',view_examtimetable,name="viewexamtimetable"),
    path('exam/update/<int:exam_id>/', update_exam , name='update_exam'),
    path('exam/delete/<int:exam_id>/', delete_exam, name='delete_exam'),

    #------------------payment-----------------

    path('payment/<int:inquiry_id>/', payment, name='payment'),
    path('payment_success/<int:inquiry_id>/', payment_success, name='payment_success'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('payment',admin_view_payment,name='admin_payment'),
    path('update/payment/<int:payment_id>/', update_payment, name='update_payment'),
    path('delete/payment/<int:payment_id>/', delete_payment, name='delete_payment'),
    
# -----------------------attendance-------------------------------
    path('mark_attendance',mark_attendance,name='mark_attendance'),
    path('student_view_attendance',student_attendance,name='student_view_attendance'),
    path('batch-wise-attendance/', batch_wise_attendance, name="batch_wise_attendance"),
    path('update-attendance/<int:attendance_id>/', admin_update_attendance, name="admin_update_attendance"),
    path('delete-attendance/<int:attendance_id>/', admin_delete_attendance, name="admin_delete_attendance"),

# --------------quiz-----------------------
     path("create_quiz/", create_quiz, name="create_quiz"),
    path("add_questions/<int:quiz_id>/", add_questions, name="add_questions"),
    path('student_quizzes/', student_view_quizzes, name="student_quizzes"),
    path('attempt_quiz/<int:quiz_id>/', attempt_quiz, name="attempt_quiz"),
    path('view_quiz_marks/', view_quiz_marks, name="view_quiz_marks"),
    path('view_quizzes/', view_quizzes, name="view_quizzes"),
    path('delete_quiz/<int:quiz_id>/', delete_quiz, name="delete_quiz"),
    path('update_quiz/<int:quiz_id>/', update_quiz, name="update_quiz"),

    path("student-forgot-password/", student_forgot_password, name="student_forgot_password"),
    path("student-reset-password/<str:token>/", student_reset_password, name="student_reset_password"),
 
    path("teacher-forgot-password/", teacher_forgot_password, name="teacher_forgot_password"),
    path("teacher-reset-password/<str:token>/", teacher_reset_password, name="teacher_reset_password"),

     path("staff-forgot-password/", staff_forgot_password, name="staff_forgot_password"),
    path("staff-reset-password/<str:token>/", staff_reset_password, name="staff_reset_password"),
   
  path('generate-report/', generate_report, name="generate_report"),
    path('process-report/', process_report, name="process_report"),
     path("fee-receipt/", generate_fee_receipt, name="fee_receipt"),


    # PDF Report URLs
   path("attendance-pdf/<int:year>/<int:month>/<int:class_id>/", generate_attendance_pdf, name="generate_attendance_pdf"),
    path("marks-pdf/<int:class_id>/<int:exam_id>/", generate_marks_pdf, name="generate_marks_pdf"),
    path("payment-pdf/<int:class_id>/", generate_payment_pdf, name="generate_payment_pdf"),
]
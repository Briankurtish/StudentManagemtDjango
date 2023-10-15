import datetime
from django.http import HttpResponse
from django.shortcuts import render

from student_management_app.models import Attendance, AttendanceReport, Courses, CustomUser, Students, Subjects


def student_home(request):
    return render(request, "student_template/student_home_template.html")


def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=Courses.objects.get(id=student.course_id.id)
    subjects=Subjects.objects.filter(course_id=course)
    return render(request, "student_template/student_view_attendance.html", {"subjects":subjects})


def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")
    
    start_data_parse=datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_obj=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_obj)
    
    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse), subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)
    
    

    return render(request, "student_template/student_attendance_data.html", {"attendance_reports":attendance_reports})

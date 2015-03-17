# Misc scripts for common wintersession tasks
from wintersession import models
from cal import mailer

# Count the number of students enrolled in at least one non-S1499 class
def countStudents():
    count = models.Student.objects.all().count()
    cs = models.Course.objects.filter(courseID='S1499')
    for s in models.Student.objects.all():
        if s.course_set.count() == 0:
            count-=1
        if set(s.course_set.all()) == set(cs):
            count-=1
    return count

# Return a list of all students enrolled in at least one non-S1499 class
def listStudents():
    students = []
    cs = models.Course.objects.filter(courseID='S1499')
    for s in models.Student.objects.all():
        if s.course_set.count() != 0 and set(s.course_set.all()) != set(cs):
            students.append(s)
    return students

# Send a bulk email
def bulkEmail(frm, to_list, subj, msg):
    for i in to_list:
        mailer.send(frm, i, subj, msg)

# Get the attendance rate for a course/day combo
# Takes arguments (Course) course  and (int) dow
def dayCourseAttendanceRate(course, dow):
    registrations = models.Registration.objects.filter(course=course)
    expected = len(registrations)
    attended = 0.0
    for r in registrations:
        if dow == 1:
            if r.attendance_M:
                attended+=1
        elif dow == 2:
            if r.attendance_Tu:
                attended+=1
        elif dow == 3:
            if r.attendance_W:
                attended+=1
        elif dow == 4:
            if r.attendance_Th:
                attended+=1
        elif dow == 5:
            if r.attendance_F:
                attended+=1
    return attended/expected

# Get the average attendance rate over all of the days that the course
# was scheduled. Takes argument (Course) course
def courseAttendanceRate(course):
    # For which days was this course scheduled?
    days = []
    for blk in course.blocks:
        days.append(blk / 1000)
    days = set(days)
    sum = 0.0
    for day in days:
        sum += dayCourseAttendanceRate(course, day)
    return sum/len(days)


from django.contrib import admin

from .models import Semester, Section, Course, Instructor, Period, Year, InstructorReview, SectionReview, CourseReview

admin.site.register(Period)
admin.site.register(Year)
admin.site.register(Semester)
admin.site.register(Section)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(CourseReview)
admin.site.register(InstructorReview)
admin.site.register(SectionReview)

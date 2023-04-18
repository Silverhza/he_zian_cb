from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from courseinfo.forms import InstructorForm, SectionForm, CourseForm, SemesterForm, RegistrationForm, StudentForm, \
    InstructorReviewForm, CourseReviewForm, SectionReviewForm
from courseinfo.models import (
    Instructor,
    Section,
    Course,
    Semester,
    Student,
    Registration,
)
from courseinfo.utils import PageLinksMixin


class InstructorList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Instructor
    permission_required = 'courseinfo.view_instructor'


class InstructorDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Instructor
    permission_required = 'courseinfo.view_instructor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instructor = self.get_object()
        section_list = instructor.sections.all()

        total_likes_dislikes = int(instructor.instructor_like) + int(instructor.instructor_dislike)
        if int(total_likes_dislikes) > 0:
            instructor_score = (int(instructor.instructor_like) / int(total_likes_dislikes)) * 100
        else:
            instructor_score = 0

        context['section_list'] = section_list
        context['instructor_score'] = round(instructor_score, 2)
        context['review_form'] = InstructorReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        form = InstructorReviewForm(request.POST)
        instructor = self.get_object()
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.instructor = instructor
            review.save()
            return redirect('courseinfo_instructor_detail_urlpattern', pk=instructor.pk)
        else:
            return self.get(request, *args, **kwargs)


class InstructorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = InstructorForm
    model = Instructor
    permission_required = 'courseinfo.add_instructor'


class InstructorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = InstructorForm
    model = Instructor
    template_name = 'courseinfo/instructor_form_update.html'
    permission_required = 'courseinfo.change_instructor'


class InstructorLikeUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        instructor = get_object_or_404(Instructor, pk=pk)
        instructor.instructor_like = int(instructor.instructor_like) + 1
        instructor.save()
        return redirect('courseinfo_instructor_detail_urlpattern', pk=instructor.pk)


class InstructorDislikeUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        instructor = get_object_or_404(Instructor, pk=pk)
        instructor.instructor_dislike = int(instructor.instructor_dislike) + 1
        instructor.save()
        return redirect('courseinfo_instructor_detail_urlpattern', pk=instructor.pk)


class InstructorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Instructor
    success_url = reverse_lazy('courseinfo_instructor_list_urlpattern')
    permission_required = 'courseinfo.delete_instructor'

    def get(self, request, pk):
        instructor = get_object_or_404(Instructor, pk=pk)
        sections = instructor.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseinfo/instructor_refuse_delete.html',
                {'instructor': instructor,
                 'sections': sections,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/instructor_confirm_delete.html',
                {'instructor': instructor}
            )


class SectionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Section
    permission_required = 'courseinfo.view_section'


class SectionDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Section
    permission_required = 'courseinfo.view_section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = self.get_object()
        semester = section.semester
        course = section.course
        instructor = section.instructor
        registration_list = section.registrations.all()
        context['semester'] = semester
        context['course'] = course
        context['instructor'] = instructor
        context['registration_list'] = registration_list

        total_likes_dislikes = int(section.section_like) + int(section.section_dislike)
        if int(total_likes_dislikes) > 0:
            section_score = (int(section.section_like) / int(total_likes_dislikes)) * 100
        else:
            section_score = 0

        context['section_score'] = round(section_score, 2)
        context['review_form'] = SectionReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SectionReviewForm(request.POST)
        section = self.get_object()
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.section = section
            review.save()
            return redirect('courseinfo_section_detail_urlpattern', pk=section.pk)
        else:
            return self.get(request, *args, **kwargs)


class SectionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = SectionForm
    model = Section
    permission_required = 'courseinfo.add_section'


class SectionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = SectionForm
    model = Section
    template_name = 'courseinfo/section_form_update.html'
    permission_required = 'courseinfo.change_section'


class SectionLikeUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        section = get_object_or_404(Section, pk=pk)
        section.section_like = int(section.section_like) + 1
        section.save()
        return redirect('courseinfo_section_detail_urlpattern', pk=section.pk)


class SectionDislikeUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        section = get_object_or_404(Section, pk=pk)
        section.section_dislike = int(section.section_dislike) + 1
        section.save()
        return redirect('courseinfo_section_detail_urlpattern', pk=section.pk)


class SectionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Section
    success_url = reverse_lazy('courseinfo_section_list_urlpattern')
    permission_required = 'courseinfo.delete_section'

    def get(self, request, pk):
        section = get_object_or_404(
            Section,
            pk=pk)
        registrations = section.registrations.all()
        if registrations.count() > 0:
            return render(
                request,
                'courseinfo/section_refuse_delete.html',
                {'section': section,
                 'registrations': registrations,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/section_confirm_delete.html',
                {'section': section}
            )


class CourseList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = 'courseinfo.view_course'


class CourseDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Course
    permission_required = 'courseinfo.view_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        section_list = course.sections.all()

        total_likes_dislikes = int(course.course_like) + int(course.course_dislike)
        if int(total_likes_dislikes) > 0:
            course_score = (int(course.course_like) / int(total_likes_dislikes)) * 100
        else:
            course_score = 0

        context['section_list'] = section_list
        context['course_score'] = round(course_score, 2)
        context['review_form'] = CourseReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CourseReviewForm(request.POST)
        course = self.get_object()
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.save()
            return redirect('courseinfo_course_detail_urlpattern', pk=course.pk)
        else:
            return self.get(request, *args, **kwargs)


class CourseCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CourseForm
    model = Course
    permission_required = 'courseinfo.add_course'


class CourseUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = CourseForm
    model = Course
    template_name = 'courseinfo/course_form_update.html'
    permission_required = 'courseinfo.change_course'


class CourseLikeUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        course = get_object_or_404(Course, pk=pk)
        course.course_like = int(course.course_like) + 1
        course.save()
        return redirect('courseinfo_course_detail_urlpattern', pk=course.pk)


class CourseDislikeUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        course = get_object_or_404(Course, pk=pk)
        course.course_dislike = int(course.course_dislike) + 1
        course.save()
        return redirect('courseinfo_course_detail_urlpattern', pk=course.pk)


class CourseDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('courseinfo_course_list_urlpattern')
    permission_required = 'courseinfo.delete_course'

    def get(self, request, pk):
        course = get_object_or_404(
            Course,
            pk=pk)
        sections = course.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseinfo/course_refuse_delete.html',
                {'course': course,
                 'sections': sections,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/course_confirm_delete.html',
                {'course': course}
            )


class SemesterList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Semester
    permission_required = 'courseinfo.view_semester'


class SemesterDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Semester
    permission_required = 'courseinfo.view_semester'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        semester = self.get_object()
        section_list = semester.sections.all()
        context['section_list'] = section_list
        return context


class SemesterCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = SemesterForm
    model = Semester
    permission_required = 'courseinfo.add_semester'


class SemesterUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = SemesterForm
    model = Semester
    template_name = 'courseinfo/semester_form_update.html'
    permission_required = 'courseinfo.change_semester'


class SemesterDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Semester
    success_url = reverse_lazy('courseinfo_semester_list_urlpattern')
    permission_required = 'courseinfo.delete_semester'

    def get(self, request, pk):
        semester = get_object_or_404(
            Semester,
            pk=pk)
        sections = semester.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseinfo/semester_refuse_delete.html',
                {'semester': semester,
                 'sections': sections,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/semester_confirm_delete.html',
                {'semester': semester}
            )


class StudentList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Student
    permission_required = 'courseinfo.view_student'


class StudentDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    permission_required = 'courseinfo.view_student'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        student = self.get_object()
        registration_list = student.registrations.all()
        context['registration_list'] = registration_list
        return context


class StudentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = StudentForm
    model = Student
    permission_required = 'courseinfo.add_student'


class StudentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = StudentForm
    model = Student
    template_name = 'courseinfo/student_form_update.html'
    permission_required = 'courseinfo.change_student'


class StudentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('courseinfo_student_list_urlpattern')
    permission_required = 'courseinfo.delete_student'

    def get(self, request, pk):
        student = get_object_or_404(
            Student,
            pk=pk)
        registrations = student.registrations.all()
        if registrations.count() > 0:
            return render(
                request,
                'courseinfo/student_refuse_delete.html',
                {'student': student,
                 'registrations': registrations,
                 }
            )
        else:
            return render(
                request,
                'courseinfo/student_confirm_delete.html',
                {'student': student}
            )


class RegistrationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Registration
    permission_required = 'courseinfo.view_registration'


class RegistrationDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Registration
    permission_required = 'courseinfo.view_registration'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        registration = self.get_object()
        student = registration.student
        section = registration.section
        context['student'] = student
        context['section'] = section
        return context


class RegistrationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = RegistrationForm
    model = Registration
    permission_required = 'courseinfo.add_registration'


class RegistrationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = RegistrationForm
    model = Registration
    template_name = 'courseinfo/registration_form_update.html'
    permission_required = 'courseinfo.change_registration'


class RegistrationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Registration
    success_url = reverse_lazy('courseinfo_registration_list_urlpattern')
    permission_required = 'courseinfo.delete_registration'
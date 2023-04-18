from django import forms
from courseinfo.models import Instructor, Section, Course, Semester, Student, Registration, InstructorReview, \
    CourseReview, SectionReview


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = '__all__'

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_disambiguator(self):
        if len(self.cleaned_data['disambiguator']) == 0:
            result = self.cleaned_data['disambiguator']
        else:
            result = self.cleaned_data['disambiguator'].strip()
        return result


class InstructorReviewForm(forms.ModelForm):
    class Meta:
        model = InstructorReview
        fields = ['comment']

    def clean_comment(self):
        return self.cleaned_data['comment'].strip()


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

    def clean_section_name(self):
        return self.cleaned_data['section_name'].strip()


class SectionReviewForm(forms.ModelForm):
    class Meta:
        model = SectionReview
        fields = ['comment']

    def clean_comment(self):
        return self.cleaned_data['comment'].strip()


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_number', 'course_name')

    def clean_course_number(self):
        return self.cleaned_data['course_number'].strip()

    def clean_course_name(self):
        return self.cleaned_data['course_name'].strip()


class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['comment']

    def clean_comment(self):
        return self.cleaned_data['comment'].strip()


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_disambiguator(self):
        if len(self.cleaned_data['disambiguator']) == 0:
            result = self.cleaned_data['disambiguator']
        else:
            result = self.cleaned_data['disambiguator'].strip()
        return result


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'

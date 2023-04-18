from django import forms
from courseinfo.models import Instructor, Section, Course, Semester, InstructorReview, CourseReview, SectionReview


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


class InstructorSearchForm(forms.Form):
    search_query = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search Instructor'})
    )


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

    def clean_section_name(self):
        return self.cleaned_data['section_name'].strip()


class SectionSearchForm(forms.Form):
    search_query = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search Section'})
    )


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


class CourseSearchForm(forms.Form):
    search_query = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Course Section'})
    )


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

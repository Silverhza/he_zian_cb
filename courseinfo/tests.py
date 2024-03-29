# blog/tests.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.test import TestCase
from .models import Period, Year, Semester, Course, Instructor, Section
from django.urls import reverse


class CourseinfoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", email="test@email.com",
            password="secret"
        )
        ci_admin_group = Group.objects.get(name='ci_admin')
        cls.user.groups.add(ci_admin_group)

        permissions = Permission.objects.filter(content_type__app_label='courseinfo')
        for permission in permissions:
            cls.user.user_permissions.add(permission)


        cls.period = Period.objects.create(
            period_id="1",
            period_sequence="1",
            period_name="Spring",
        )

        cls.year = Year.objects.create(
            year_id="1",
            year=2022,
        )

        cls.semester = Semester.objects.create(
            semester_id="1",
            year=cls.year,
            period=cls.period,
        )

        cls.course = Course.objects.create(
            course_id="1",
            course_number="IS439",
            course_name="Web Development Using Application Frameworks",
        )

        cls.instructor = Instructor.objects.create(
            instructor_id="300",
            first_name="John",
            last_name="Smith",
        )

        cls.section = Section.objects.create(
            section_id="1",
            section_name="section 1",
            semester=cls.semester,
            course=cls.course,
            instructor=cls.instructor,
        )

    def test_period_model(self):
        self.client.login(username="testuser", password="secret")
        self.assertEqual(str(self.period.period_id), "1")
        self.assertEqual(str(self.period.period_sequence), "1")
        self.assertEqual(self.period.period_name, "Spring")

    def test_year_model(self):
        self.client.login(username="testuser", password="secret")
        self.assertEqual(str(self.year.year_id), "1")
        self.assertEqual(self.year.year, 2022)

    def test_semester_model(self):
        self.client.login(username="testuser", password="secret")
        self.assertEqual(str(self.semester.semester_id), "1")
        self.assertEqual(str(self.semester.year.year_id), "1")
        self.assertEqual(self.semester.year.year, 2022)
        self.assertEqual(str(self.semester.period.period_id), "1")
        self.assertEqual(str(self.semester.period.period_sequence), "1")
        self.assertEqual(self.semester.period.period_name, "Spring")
        self.assertEqual(self.semester.get_absolute_url(), "/semester/1/")

    def test_course_model(self):
        self.client.login(username="testuser", password="secret")
        self.assertEqual(str(self.course.course_id), "1")
        self.assertEqual(str(self.course.course_number), "IS439")
        self.assertEqual(self.course.course_name, "Web Development Using Application Frameworks")
        self.assertEqual(self.course.get_absolute_url(), "/course/1/")

    def test_instructor_model(self):
        self.client.login(username="testuser", password="secret")
        self.assertEqual(str(self.instructor.instructor_id), "300")
        self.assertEqual(self.instructor.first_name, "John")
        self.assertEqual(self.instructor.last_name, "Smith")
        self.assertEqual(self.instructor.get_absolute_url(), "/instructor/300/")

    def test_section_model(self):
        self.client.login(username="testuser", password="secret")
        self.assertEqual(str(self.section.section_id), "1")
        self.assertEqual(self.section.section_name, "section 1")
        self.assertEqual(str(self.section.semester.semester_id), "1")
        self.assertEqual(str(self.section.semester.year.year_id), "1")
        self.assertEqual(self.section.semester.year.year, 2022)
        self.assertEqual(str(self.section.semester.period.period_id), "1")
        self.assertEqual(str(self.section.semester.period.period_sequence), "1")
        self.assertEqual(self.section.semester.period.period_name, "Spring")
        self.assertEqual(str(self.section.course.course_id), "1")
        self.assertEqual(str(self.section.course.course_number), "IS439")
        self.assertEqual(self.section.course.course_name, "Web Development Using Application Frameworks")
        self.assertEqual(str(self.section.instructor.instructor_id), "300")
        self.assertEqual(self.section.instructor.first_name, "John")
        self.assertEqual(self.section.instructor.last_name, "Smith")
        self.assertEqual(self.section.get_absolute_url(), "/section/1/")

    def test_instructor_list_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_instructor_list_urlpattern"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")
        self.assertTemplateUsed(response, "courseinfo/instructor_list.html")

    def test_section_list_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_section_list_urlpattern"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "section 1")
        self.assertTemplateUsed(response, "courseinfo/section_list.html")

    def test_course_list_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_course_list_urlpattern"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "IS439")
        self.assertTemplateUsed(response, "courseinfo/course_list.html")

    def test_semester_list_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_semester_list_urlpattern"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")
        self.assertTemplateUsed(response, "courseinfo/semester_list.html")

    def test_instructor_detail_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_instructor_detail_urlpattern",
                                           kwargs={"pk": self.instructor.pk}))
        no_response = self.client.get("/instructor/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Smith")
        self.assertTemplateUsed(response, "courseinfo/instructor_detail.html")

    def test_section_detail_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_section_detail_urlpattern",
                                           kwargs={"pk": self.section.pk}))
        no_response = self.client.get("/section/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "section 1")
        self.assertTemplateUsed(response, "courseinfo/section_detail.html")

    def test_course_detail_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_course_detail_urlpattern",
                                           kwargs={"pk": self.course.pk}))
        no_response = self.client.get("/course/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "IS439")
        self.assertTemplateUsed(response, "courseinfo/course_detail.html")

    def test_semester_detail_view(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(reverse("courseinfo_semester_detail_urlpattern",
                                           kwargs={"pk": self.semester.pk}))
        no_response = self.client.get("/semester/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "1")
        self.assertTemplateUsed(response, "courseinfo/semester_detail.html")

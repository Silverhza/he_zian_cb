from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    instructor_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                             content_type__model='instructor')

    period_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                         content_type__model='period')

    year_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                       content_type__model='year')

    semester_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                           content_type__model='semester')

    course_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                         content_type__model='course')

    coursereview_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                               content_type__model='coursereview')

    instructorreview_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                                   content_type__model='instructorreview')

    sectionreview_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                                content_type__model='sectionreview')

    section_permissions = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                          content_type__model='section')

    perm_view_instructor = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                           content_type__model='instructor',
                                                           codename='view_instructor')

    perm_view_period = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                       content_type__model='period',
                                                       codename='view_period')

    perm_view_year = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                     content_type__model='year',
                                                     codename='view_year')

    perm_view_semester = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                         content_type__model='semester',
                                                         codename='view_semester')

    perm_view_course = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                       content_type__model='course',
                                                       codename='view_course')

    perm_view_section = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                        content_type__model='section',
                                                        codename='view_section')

    perm_view_coursereview = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                             content_type__model='coursereview',
                                                             codename='view_coursereview')

    perm_view_instructorreview = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                                 content_type__model='instructorreview',
                                                                 codename='view_instructorreview')

    perm_view_sectionreview = permission_class.objects.filter(content_type__app_label='courseinfo',
                                                              content_type__model='sectionreview',
                                                              codename='view_sectionreview')
    ci_user_permissions = chain(perm_view_instructor,
                                perm_view_period,
                                perm_view_year,
                                perm_view_semester,
                                perm_view_course,
                                perm_view_section,
                                perm_view_coursereview,
                                perm_view_instructorreview,
                                perm_view_sectionreview,
                                coursereview_permissions,
                                instructorreview_permissions,
                                sectionreview_permissions,)

    ci_admin_permissions = chain(instructor_permissions,
                                 period_permissions,
                                 year_permissions,
                                 semester_permissions,
                                 course_permissions,
                                 section_permissions,
                                 perm_view_coursereview,
                                 perm_view_instructorreview,
                                 perm_view_sectionreview,
                                 coursereview_permissions,
                                 instructorreview_permissions,
                                 sectionreview_permissions,)

    my_groups_initialization_list = [
        {
            "name": "ci_user",
            "permissions_list": ci_user_permissions,
        },
        {
            "name": "ci_admin",
            "permissions_list": ci_admin_permissions,
        },
    ]
    return my_groups_initialization_list


def add_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            group_object.permissions.set(group['permissions_list'])
            group_object.save()


def remove_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    group_model_class = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = group_model_class.objects.get(
                name=group['name']
            )
            list_of_permissions = group['permissions_list']
            for permission in list_of_permissions:
                group_object.permissions.remove(permission)
                group_object.save()


class Migration(migrations.Migration):
    dependencies = [
        ('courseinfo', '0005_create_groups'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions_data,
            remove_group_permissions_data
        )
    ]

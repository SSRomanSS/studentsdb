# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Students
def students_list(request):
    students = (
        {
            'id': 1,
            'first_name': 'Віталій',
            'last_name': 'Подоба',
            'ticket': 235,
            'image': 'img/me.jpeg'
        },
        {
            'id': 2,
            'first_name': 'Корост',
            'last_name': 'Андрій',
            'ticket': 2123,
            'image': 'img/piv.png'
        },
        {
            'id': 3,
            'first_name': 'Притула',
            'last_name': 'Тарас',
            'ticket': 5332,
            'image': 'img/podoba3.jpg'
        }
    )
    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student {}</h1>'.format(sid))


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student {}</h1>'.format(sid))


# Views for Groups
def groups_list(request):
    groups = (
        {
            'id': 1,
            'name': 'МтМ-21',
            'leader': 'Ячменев Олег',
        },
        {
            'id': 2,
            'name': 'МтМ-22',
            'leader': 'Віталій Подоба',
        },
        {
            'id': 3,
            'name': 'МтМ-23',
            'leader': 'Іванов Андрій',
        }
    )
    return render(request, 'students/groups_list.html', {'groups': groups})


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group {}</h1>'.format(gid))


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group {}/h1>'.format(gid))


def students_visiting(request):
    return HttpResponse('<h1>Student Visiting</h1>')


def student_visiting(request, sid):
    return HttpResponse('<h1>Student {} Visiting</h1>'.format(sid))

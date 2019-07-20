# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


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
    return HttpResponse('<h1>Delete Group {}</h1>'.format(gid))

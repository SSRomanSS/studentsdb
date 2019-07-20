# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Journal:
def students_visiting(request):
    return HttpResponse('<h1>Student Visiting</h1>')


def student_visiting(request, sid):
    return HttpResponse('<h1>Student {} Visiting</h1>'.format(sid))

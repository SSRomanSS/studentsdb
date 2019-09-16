# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from ..models.groups import Group
from ..models.students import Student


# Views for Groups
def groups_list(request):
    groups = Group.objects.all()
    
    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
    if request.GET.get('reverse', '') == '1':
        groups = groups.reverse()
    
    # paginate students
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        groups = paginator.page(paginator.num_pages)
    return render(request, 'students/groups_list.html', {'groups': groups})


class StudentsOfGroup(ListView):
    # model = Student
    template_name = 'students/students_in_group.html'
    context_object_name = 'students'  # instead of object_list
    ordering = ['last_name']
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super(StudentsOfGroup, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']  # additional variable in context to use it in template
        pk = int(context['slug'])
        context['group'] = Group.objects.get(pk=pk).title  # additional variable in context to use it in template
        return context

    def get_queryset(self):  # instead of 'model=Student'
        students = Student.objects.filter(student_group=self.kwargs['slug'])
        return students
    
        
def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group {}</h1>'.format(gid))


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group {}</h1>'.format(gid))

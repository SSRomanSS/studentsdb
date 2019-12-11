# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView, CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions

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


class GroupAddForm(ModelForm):
	class Meta:
		model = Group
		fields = ['title']
	
	def __init__(self, *args, **kwargs):
		super(GroupAddForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		# set form tag attributes
		self.helper.form_action = reverse('groups_add')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		# self.helper.render_unmentioned_fields = True
		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		# add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button', 'Зберегти'),
			HTML('<button type="submit" formnovalidate name="cancel_button"'
				'class="btn btn-link" value="Скасувати">Скасувати</button>')
			)
		)
		# self.helper.add_input(Submit('add_button', 'Зберегти'))
		# self.helper.add_input(Submit('cancel_button', 'Скасувати', css_class='btn btn-link'))


class GroupsAddView(CreateView):
	model = Group
	template_name = 'groups/groups_add.html'
	form_class = GroupAddForm
	# fields = '__all__'
	
	def get_success_url(self):
		return '{}?status_message=Групу успішно збережено!'.format(reverse('groups'))
	
	# TODO add validation to prevent group diplicate creation
	
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect('{}?status_message=Cтворення групи скасовано!'.format(reverse('groups')))
		else:
			return super(GroupsAddView, self).post(request, *args, **kwargs)


def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group {}</h1>'.format(gid))


def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group {}</h1>'.format(gid))

# -*- coding: utf-8 -*-

from datetime import datetime
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions


from ..models.students import Student
from ..models.groups import Group


# Views for Students
def students_list(request):
	students = Student.objects.all()
	
	# try to order students list
	order_by = request.GET.get('order_by', '')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
	if request.GET.get('reverse', '') == '1':
		students = students.reverse()
	
	# paginate students
	paginator = Paginator(students, 3)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		students = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		students = paginator.page(paginator.num_pages)
	return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
	# was form posted?
	if request.method == 'POST':
		# was form add button clicked?
		if request.POST.get('add_button') is not None:
			# validate student data will go here
			errors = {}
			data = {'middle_name': request.POST.get('middle_name'),
					'notes': request.POST.get('notes')}
			# validate user input
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = "Ім'я є обов'язковим"
			else:
				data['first_name'] = first_name
		
			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = "Прізвище є обов'язковим"
			else:
				data['last_name'] = last_name
	
			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = "Дата народження є обов'язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = "Введіть коректний формат дати(напр. 1984 - 12 - 30)"
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = "Номер білета є обов'язковим"
			else:
				data['ticket'] = ticket
				
			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = "Оберіть групу для студента"
			else:
				data['student_group'] = Group.objects.get(pk=student_group)

			photo = request.FILES.get('photo')
			if photo:
				try:
					Image.open(photo).verify()
				except Exception:
					errors['photo'] = "Файл не є зображенням"
				else:
					if photo.size > (2 * 1024 * 1024):
						errors['photo'] = "Завеликий файл. Фото має бути не більше 2 мегабайт"
					else:
						data['photo'] = photo

			# save student
			if not errors:
				student = Student(**data)
				student.save()
				# redirect to students list
				return HttpResponseRedirect('{}?status_message=Студента {} успішно додано'.format(reverse('home'), student))
			else:
				# render form with errors and previos ser inpt
				return render(request, 'students/students_add.html',
					{'groups': Group.objects.all().order_by('title'),
					'errors': errors})
		elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
			return HttpResponseRedirect('{}?status_message=Додавання студента скасовано!'.format(reverse('home')))
	else:
		# initial form render
		return render(
			request,
			'students/students_add.html',
			{'groups': Group.objects.all().order_by('title')}
		)


class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		
	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		# set form tag attributes
		self.helper.form_action = reverse('students_edit', args=[self.instance.id])
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		self.helper.render_unmentioned_fields = True
		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		# add buttons
		self.helper.layout.append(FormActions(
			Submit('add_button', 'Зберегти'),
			HTML('<button type="submit" name="cancel_button" class="btn btn-link" value="Скасувати">Скасувати</button>')
			)
		)
		# self.helper.add_input(Submit('add_button', 'Зберегти'))
		# self.helper.add_input(Submit('cancel_button', 'Скасувати', css_class='btn btn-link'))
		
		
class StudentUpdateView(UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
	form_class = StudentUpdateForm
	# fields = '__all__'
	
	def get_success_url(self):
		return '{}?status_message=Студента успішно збережено!'.format(reverse('home'))

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			return HttpResponseRedirect('{}?status_message=Редагування студента скасовано!'.format(reverse('home')))
		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)

# def students_edit(request, sid):
# return HttpResponse('<h1>Edit Student {}</h1>'.format(sid))


class StudentDeleteView(DeleteView):
	model = Student
	template_name = 'students/students_confirm_delete.html'
	
	def get_success_url(self):
		return '{}?status_message=Студента успішно видалено!'.format(reverse('home'))

# def students_delete(request, sid):
# return HttpResponse('<h1>Delete Student {}</h1>'.format(sid))

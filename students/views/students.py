# -*- coding: utf-8 -*-

from datetime import datetime
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student {}</h1>'.format(sid))


def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student {}</h1>'.format(sid))

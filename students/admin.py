# -*- coding: utf-8 -*-
from functools import partial
from django.contrib import admin
from django.urls import reverse
from django.forms import ModelForm, ValidationError, BaseModelFormSet


from .models.groups import Group
from .models.students import Student


class StudentFormAdmin(ModelForm):
	def clean_student_group(self):
		"""Check if student is leader in any group. If yes, then ensure it’s the same as selected group."""
		# get group where current student is a leader
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError('Студент є старостою іншої групи.', code='invalid')
		return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
	list_display = ['last_name', 'first_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['last_name']
	list_filter = ['student_group']
	list_per_page = 10
	search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
	form = StudentFormAdmin
	
	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk': obj.id})


class GroupFormAdmin(ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['leader'].queryset = Student.objects.filter(
			student_group=self.instance)
	
	def clean_leader(self):
		"""Check if student is leader in any group. If yes, then ensure it’s the same as selected group."""
		# get group where current student is a leader
		students = Student.objects.filter(student_group=self.instance)
		if self.cleaned_data['leader'] not in students:
			raise ValidationError('Студент не є членом групи.', code='invalid')
		return self.cleaned_data['leader']


class GroupAdmin(admin.ModelAdmin):
	
	form = GroupFormAdmin
	list_display = ['title', 'leader']
	list_display_links = ['title']
	#list_editable = ['leader']
	ordering = ['title']
	list_per_page = 10
	search_fields = ['title', 'leader']
	
	
# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)

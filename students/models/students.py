# -*- coding: utf-8 -*-

from django.db import models


# Create your models here.
class Student(models.Model):
	"""Student Model"""
	
	class Meta(object):
		verbose_name = 'Студент'
		verbose_name_plural = 'Студенти'
		ordering = ['last_name']
	
	first_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name='Ім’я')
	
	last_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name='Прізвище')
	
	middle_name = models.CharField(
		max_length=256,
		blank=True,
		verbose_name='По-батькові',
		default='')
	
	birthday = models.DateField(
		blank=False,
		verbose_name='Дата народження',
		null=True)
	
	photo = models.ImageField(
		blank=True,
		verbose_name='Фото',
		null=True)
	
	ticket = models.CharField(
		max_length=256,
		blank=False,
		verbose_name='Білет')
	
	notes = models.TextField(
		blank=True,
		verbose_name='Додаткові нотатки')
	
	student_group = models.ForeignKey(
		'Group',
		verbose_name='Група',
		blank=False,
		null=True,
		on_delete=models.PROTECT)
	
	def __str__(self):
		return '{} {}'.format(self.first_name, self.last_name)

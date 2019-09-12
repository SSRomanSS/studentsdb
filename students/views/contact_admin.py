# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from studentsdb.settings import ADMIN_EMAIL


class ContactForm(forms.Form):
	
	from_email = forms.EmailField(
		label="E-mail адреса")
	subject = forms.CharField(
		label="Заголовок листа",
		max_length=128)
	message = forms.CharField(
		label="Текст повідомлення",
		max_length=2560,
		widget=forms.Textarea,
		help_text='Максимум 2560 символів')
	
	def __init__(self, *args, **kwargs):
		# call original initializator
		super(ContactForm, self).__init__(*args, **kwargs)
		# this helper object allows us to customize form
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_action = reverse('contact_admin')
		self.helper.render_unmentioned_fields = True
		# self.disable_csrf = False
		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2'
		self.helper.field_class = 'col-sm-10'
		
		self.helper.layout = Layout(
			Field('subject', placeholder='Заголовок'),
			Field('from_email', placeholder='E-mail адреса'),
			Field('message', placeholder='Введіть текст повідомлення')
			# Submit('submit', 'Sign up')
		)
		
		# form buttons
		self.helper.add_input(Submit('send_button', 'Надіслати'))
	

def contact_admin(request):
	# check if form was posted
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = ContactForm(request.POST)
		# check whether user data is valid:
		if form.is_valid():
			# send email
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			from_email = form.cleaned_data['from_email']
			
			try:
				send_mail(subject, message, from_email, [ADMIN_EMAIL])
			except Exception:
				message = 'Під час відправки листа виникла непередбачувана помилка. Спробуйте скористатись даною формою пізніше.'
			else:
				message = 'Повідомлення успішно надіслане!'
			# redirect to same contact page with success message
			return HttpResponseRedirect('{}?status_message={}'.format(reverse('contact_admin'), message))

	# if there was not POST render blank form
	else:
		form = ContactForm()
	return render(request, 'contact_admin/form.html', {'form': form})
	


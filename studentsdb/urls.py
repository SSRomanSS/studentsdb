"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
# from django.conf import settings
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static
from django.views.static import serve
from .settings import MEDIA_ROOT, DEBUG
from students.views import students, groups, journal, contact_admin

urlpatterns = [
	re_path(r'^$', students.students_list, name='home'),
	re_path(r'^students/add/$', students.students_add, name='students_add'),
	re_path(r'^students/(?P<pk>\d+)/edit/$', students.StudentUpdateView.as_view(), name='students_edit'),
	re_path(r'^students/(?P<pk>\d+)/delete/$', students.StudentDeleteView.as_view(), name='students_delete'),

	re_path(r'^groups/$', groups.groups_list, name='groups'),
	re_path(r'^groups/add/$', groups.GroupsAddView.as_view(), name='groups_add'),
	re_path(r'^groups/(?P<gid>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
	re_path(r'^groups/(?P<slug>\d+)/students/$', groups.StudentsOfGroup.as_view(), name='groups_students'),
	re_path(r'^groups/(?P<gid>\d+)/delete/$', groups.groups_delete, name='groups_delete'),

	re_path(r'^journal/$', journal.students_visiting, name='students_visiting'),
	re_path(r'^journal/(?P<sid>\d+)/visiting$', journal.student_visiting, name='student_visiting'),
	
	# Contact Admin Form
	re_path(r'^contact-admin/$', contact_admin.contact_admin, name='contact_admin'),

	path('admin/', admin.site.urls),
]

if DEBUG:
	urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT, }), ]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

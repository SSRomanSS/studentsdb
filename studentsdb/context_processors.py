from .settings import MEDIA_URL

def students_processor(request):
	if request.is_secure():
		scheme = 'https'
	else:
		scheme = 'http'
	PORTAL_URL = '{}://{}'.format(scheme, request.get_host())
	return {'PORTAL_URL': PORTAL_URL}


def media_processor(request):
	return {'MEDIA_URL': MEDIA_URL}

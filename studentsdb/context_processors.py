def students_processor(request):
	if request.is_secure():
		scheme = 'https'
	else:
		scheme = 'http'
	PORTAL_URL = '{}://{}'.format(scheme, request.get_host())
	return {'PORTAL_URL': PORTAL_URL}

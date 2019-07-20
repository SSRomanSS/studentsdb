def students_processor(request):
	scheme = 'https' if request.is_secure() else 'http'
	PORTAL_URL = '{}://{}'.format(scheme, request.get_host())
	return {'PORTAL_URL': PORTAL_URL}

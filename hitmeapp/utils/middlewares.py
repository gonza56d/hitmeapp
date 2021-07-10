"""Utility middlewares."""

# Project
from hitmeapp.assetservices.models import get_services_list
from hitmeapp.users.forms import LoginForm


class UniversalVariablesMiddleware:
	"""Set the request variables that will be required in all the views (or in
	most of them)."""

	def __init__(self, get_response) -> None:
		self.get_response = get_response

	def __call__(self, request) -> None:
		request.login_form = LoginForm(prefix='login')
		if request.user.is_authenticated:
			request.asset_services_list = get_services_list()
		return self.get_response(request)

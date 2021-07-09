"""Utility middlewares."""

# Project
from hitmeapp.users.forms import LoginForm


class LoginFormMiddleware:
	"""Set LoginForm available in all the requests."""

	def __init__(self, get_response) -> None:
		self.get_response = get_response

	def __call__(self, request) -> None:
		request.login_form = LoginForm(prefix='login')
		return self.get_response(request)

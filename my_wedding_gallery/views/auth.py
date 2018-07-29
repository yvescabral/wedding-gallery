from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config
from ..models import User
from ..security import check_password, hash_password


class AuthViews:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='login', renderer='../templates/login.jinja2')
    def login_view(self):
        next = self.request.params.get('next') or self.request.route_url('home')
        email = ''
        did_fail = False
        if 'submit' in self.request.POST:
            email = self.request.POST.get('email', '')
            password = self.request.POST.get('password', '')
            query = self.request.dbsession.query(User)
            user = query.filter_by(email=email).first()
            if user and check_password(password, user.password):
                headers = remember(self.request, email)
                return HTTPFound(location=next, headers=headers)
            did_fail = True
        return {
            'email': email,
            'next': next,
            'failed_attempt': did_fail,
        }

    @view_config(route_name='register', renderer='../templates/register.jinja2')
    def register_view(self):
        name, email, message = '', '', ''
        if 'submit' in self.request.POST:
            name = self.request.POST.get('name', '')
            email = self.request.POST.get('email', '')
            password = self.request.POST.get('password', '')
            password_confirmation = self.request.POST.get('password_confirmation', '')
            if not name or not email or not password or not password_confirmation:
                message = 'You must complete all fields.'
            elif password != password_confirmation:
                message = 'The password confirmation does not match.'
            else:
                user = User(name=name, email=email, password=hash_password(password))
                self.request.dbsession.add(user)
                headers = remember(self.request, email)
                return HTTPFound(location=self.request.route_url('home'), headers=headers)
        return {
            'name': name,
            'email': email,
            'message': message
        }

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url, headers=headers)

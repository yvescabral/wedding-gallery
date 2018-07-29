from pyramid.security import authenticated_userid
from pyramid.view import forbidden_view_config, notfound_view_config
from pyramid.httpexceptions import HTTPForbidden, HTTPFound


@forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {}
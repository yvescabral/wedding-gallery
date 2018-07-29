from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from .security import RequestWithUserAttribute, group_finder
from .resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['bcrypt.secret'], callback=group_finder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.set_request_factory(RequestWithUserAttribute)

    config.set_root_factory(Root)

    config.include('pyramid_jinja2')
    config.include('pyramid_services')
    config.include('pyramid_boto3')
    config.include('.models')
    config.include('.routes')

    config.scan()
    return config.make_wsgi_app()

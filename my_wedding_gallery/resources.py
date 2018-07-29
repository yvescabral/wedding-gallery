from pyramid.security import (
    Allow,
    Authenticated,
)
from .models import Photo

class Root:
    __acl__ = [
        (Allow, Authenticated, 'create'),
        (Allow, 'g:admin', 'manage'),
    ]

    waiting_photos_count = 0

    def __init__(self, request):
        self.request = request
        if request.user and 'admin' in request.user.groups:
            self.waiting_photos_count = self.request.dbsession.query(Photo).filter_by(approved=None).count()
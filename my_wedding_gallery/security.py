from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid
from .models import User
import bcrypt


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def check_password(pw, hashed_pw):
    expected_hash = hashed_pw.encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)


def group_finder(userid, request):
    if request.user:
        return ['g:%s' % g for g in request.user.groups]


class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        query = self.dbsession.query(User)
        userid = unauthenticated_userid(self)
        if userid is not None:
            # this should return None if the user doesn't exist
            # in the database
            return query.filter_by(email=userid).first()

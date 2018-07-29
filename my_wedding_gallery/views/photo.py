from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk, HTTPNotFound
from ..models import Photo, Like
import transaction


class PhotoViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='approve', permission='manage')
    @view_config(route_name='decline', permission='manage')
    @view_config(route_name='like', permission='create')
    @view_config(route_name='unlike', permission='create')
    def action(self):
        query = self.request.dbsession.query(Photo)
        photo = query.filter_by(id=self.request.matchdict['photo_id']).first()
        if photo:
            with transaction.manager:
                if self.request.matched_route.name == 'approve':
                    photo.approved = True
                elif self.request.matched_route.name == 'decline':
                    photo.approved = False
                elif self.request.matched_route.name == 'like':
                    like = Like(photo_id=photo.id, user_id=self.request.user.id)
                    self.request.dbsession.add(like)
                elif self.request.matched_route.name == 'unlike':
                    query = self.request.dbsession.query(Like)
                    like = query.filter_by(photo_id=photo.id, user_id=self.request.user.id).first()
                    self.request.dbsession.delete(like)
            return HTTPOk()
        return HTTPNotFound()

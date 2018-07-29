from pyramid.view import view_config
from sqlalchemy import func

from ..models import Photo, Like

from uuid import uuid4
from datetime import datetime
from PIL import Image
import shutil
import transaction
import logging
log = logging.getLogger(__name__)


class GalleryViews:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(route_name='home', renderer='../templates/home.jinja2')
    def home_view(self):
        session = self.request.dbsession
        stmt = session.query(Photo, func.count(Like.user_id).label('total')).filter_by(approved=True)\
            .join(Like).group_by(Photo).order_by('total DESC').subquery()
        photos_likes = session.query(Photo, stmt.c.total).filter(Photo.approved).outerjoin(stmt, Photo.id == stmt.c.id)
        user_liked_photos = []
        if self.request.user:
            user_liked_photos = session.query(Like.photo_id).filter_by(user_id=self.request.user.id).all()
            user_liked_photos = [t[0] for t in user_liked_photos]
        return {'photos_likes': photos_likes, 'user_liked_photos': user_liked_photos}

    @view_config(route_name='my_photos', renderer='../templates/my_photos.jinja2', permission='create')
    def my_photos_view(self):
        if 'submit' in self.request.POST:
            client = self.request.find_service(name='boto3.client.filepot')
            bucket = 'my-wedding-gallery'
            files = self.request.POST.getall('files')
            with transaction.manager:
                for f in files:
                    filename = "%s" % uuid4()
                    temp = "/tmp/%s" % filename
                    with open(temp, 'wb') as output_file:
                        shutil.copyfileobj(f.file, output_file)

                    size = 350, 350
                    image = Image.open(temp)
                    image.thumbnail(size)
                    temp_thumb = temp + "_t"
                    image.save(temp_thumb, 'png')

                    client.upload_file(temp, bucket, "photos/%s" % filename)
                    client.upload_file(temp_thumb, bucket, "photos/%s_t" % filename)
                    photo = Photo(
                        filename=filename,
                        user_id=self.request.user.id,
                        uploaded_at=datetime.now(),
                        approved=True if 'admin' in self.request.user.groups else False
                    )
                    self.request.dbsession.add(photo)
        return {}

    @view_config(route_name='manage', renderer='../templates/manage.jinja2', permission='manage')
    def manage_view(self):
        query = self.request.dbsession.query(Photo)
        waiting_photos = query.filter_by(approved=None).all()
        approved_photos = query.filter_by(approved=True).all()
        declined_photos = query.filter_by(approved=False).all()
        return {
            'waiting_photos': waiting_photos,
            'approved_photos': approved_photos,
            'declined_photos': declined_photos,
        }

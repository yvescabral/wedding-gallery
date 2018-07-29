import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from my_wedding_gallery.models.meta import Base
from my_wedding_gallery.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models import User
from ..security import hash_password

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        db_session = get_tm_session(session_factory, transaction.manager)

        husband_user = User(name='Husband', email='husband@family.com', password=hash_password('husband'), groups=['admin'])
        wife_user = User(name='Wife', email='wife@family.com', password=hash_password('wife'), groups=['admin'])
        db_session.add(husband_user)
        db_session.add(wife_user)

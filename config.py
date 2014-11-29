import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WTF_CSRF_ENABLED = True
SECRET_KEY = '\xe9\xc8\x1b\x8f\x1c\xaa\x82X\xb0\xb8\xa0`\xbc\x98z\x82\xe1#~9\xda\x85a\xf9'
# lavatar settings file for docker

import os

from ssl import CERT_NONE


BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ.get('DEBUG', False)

# Redis Settings
# ==============

REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')
REDIS_DATABASE = os.environ.get('REDIS_DATABASE', 0)

# LDAP Settings
# =============

LDAP_SERVER = os.environ.get('LDAP_SERVER', 'localhost')
LDAP_BINDDN = os.environ.get('LDAP_BINDDN', '')
LDAP_SECRET = os.environ.get('LDAP_SECRET', '')
LDAP_USE_TLS = os.environ.get('LDAP_USETLS', True)
LDAP_REQUIRE_CERT = CERT_NONE
LDAP_USER_BASEDN = os.environ.get('LDAP_USER_BASEDN',
                                  'ou=people,dc=example,dc=com')
LDAP_USER_OBJECTCLASS = os.environ.get('LDAP_USER_OBJECTCLASS',
                                       'inetOrgPerson')
LDAP_USER_SEARCHFILTER = os.environ.get('LDAP_USER_SEARCHFILTER', '')
LDAP_USER_ATTR_MAIL = os.environ.get('LDAP_USER_ATTR_MAIL', 'mail')
LDAP_USER_ATTR_PHOTO = os.environ.get('LDAP_USER_ATTR_PHOTO', 'jpegPhoto')

# E-Mail MD5 Database Settings
# ============================

MD5DB_ENTRY_TTL = int(os.environ.get('MD5DB_ENTRY_TTL', 7200))
MD5DB_THREAD_TIMER = int(os.environ.get('MD5DB_THREAD_TIMER', 3600))


# Avatar settings
# ===============

# Redis
AVATAR_TTL = int(os.environ.get('AVATAR_TTL', 21600))

# Image
AVATAR_STATIC = os.path.join(BASEDIR, 'app', 'static', 'img')
AVATAR_STATIC_IMAGES = {'mm': 'no_avatar.jpg'}
AVATAR_DEFAULT_IMAGE = os.environ.get('AVATAR_DEFAULT_IMAGE', 'mm')
AVATAR_DEFAULT_SIZE = int(os.environ.get('AVATAR_DEFAULT_SIZE', 80))
AVATAR_MAX_SIZE = int(os.environ.get('AVATAR_MAX_SIZE', 1024))
AVATAR_DEFAULT_METHOD = os.environ.get('AVATAR_DEFAULT_METHOD', 'thumbnail')

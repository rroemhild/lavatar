# -*- coding: utf-8 -*-

# Redis Settings
# ==============

REDIS_URL = 'redis://localhost:6379'
REDIS_DATABASE = 0

# LDAP Settings
# =============

# LDAP Server
LDAP_SERVER = 'localhost'
LDAP_BINDDN = 'cn=admin,dc=example,dc=com'
LDAP_SECRET = 'secret'
LDAP_USE_TLS = True

# User
LDAP_USER_BASEDN = 'ou=people,dc=example,dc=com'
LDAP_USER_OBJECTCLASS = 'inetOrgPerson'
LDAP_USER_SEARCHFILTER = '(objectClass=*)'
LDAP_USER_ATTR_MAIL = 'mail'
LDAP_USER_ATTR_PHOTO = 'jpegPhoto'

# E-Mail MD5 Database Settings
# ============================

MD5DB_ENTRY_TTL = 36000  # seconds
MD5DB_THREAD_TIMER = 60  # update frequency in minutes

# Avatar settings
# ===============

# Redis Cache
AVATAR_TTL = 3600  # seconds

# Image
AVATAR_STATIC_IMAGES = {'mm': 'no_avatar.jpg'}  # map images from static/img
AVATAR_DEFAULT_IMAGE = 'mm'  # default image on AVATAR_STATIC_IMAGES
AVATAR_DEFAULT_SIZE = 80  # default image size per request
AVATAR_MAX_SIZE = 1024  # max image size per request
AVATAR_CROP_TYPE = 'top'  # set to top, middle or bottom

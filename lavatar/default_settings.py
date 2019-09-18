# lavatar settings file for docker

import os

from ssl import CERT_NONE


BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ.get("DEBUG", False)

# Redis Settings
# ==============

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379")
REDIS_DATABASE = os.environ.get("REDIS_DATABASE", 0)

# LDAP Settings
# =============

LDAP_SERVER = os.environ.get("LDAP_SERVER", "localhost")
LDAP_BINDDN = os.environ.get("LDAP_BINDDN", "")
LDAP_SECRET = os.environ.get("LDAP_SECRET", "")
LDAP_USE_TLS = os.environ.get("LDAP_USETLS", True)
LDAP_REQUIRE_CERT = CERT_NONE
LDAP_USER_BASEDN = os.environ.get("LDAP_USER_BASEDN", "ou=people,dc=example,dc=com")
LDAP_USER_OBJECTCLASS = os.environ.get("LDAP_USER_OBJECTCLASS", "inetOrgPerson")
LDAP_USER_SEARCHFILTER = os.environ.get("LDAP_USER_SEARCHFILTER", "")
LDAP_USER_ATTR_MAIL = os.environ.get("LDAP_USER_ATTR_MAIL", "mail")
# LDAP_USER_ATTR_MAIL = os.environ.get('LDAP_USER_ATTR_MAIL', ['mail', 'alias', 'mailAlternateAddress'])
LDAP_USER_ATTR_PHOTO = os.environ.get("LDAP_USER_ATTR_PHOTO", "jpegPhoto")

# E-Mail MD5 Database Settings
# ============================

MD5DB_ENTRY_TTL = int(os.environ.get("MD5DB_ENTRY_TTL", 7200))
MD5DB_THREAD_TIMER = int(os.environ.get("MD5DB_THREAD_TIMER", 3600))


# Avatar settings
# ===============

# Redis
AVATAR_TTL = int(os.environ.get("AVATAR_TTL", 21600))

# Image
AVATAR_STATIC = os.path.join(BASEDIR, "static", "img")
AVATAR_STATIC_IMAGES = {"mm": "no_avatar.jpg", "no_avatar": "no_avatar.jpg"}
AVATAR_DEFAULT_IMAGE = os.environ.get("AVATAR_DEFAULT_IMAGE", "no_avatar")
AVATAR_DEFAULT_SIZE = int(os.environ.get("AVATAR_DEFAULT_SIZE", 80))
AVATAR_MAX_SIZE = int(os.environ.get("AVATAR_MAX_SIZE", 1024))
AVATAR_DEFAULT_METHOD = os.environ.get("AVATAR_DEFAULT_METHOD", "thumbnail")

# Identicon
AVATAR_IDENTICON_ENABLE = os.environ.get("AVATAR_IDENTICON_ENABLE", "true")
AVATAR_IDENTICON_CACHE = os.environ.get("AVATAR_IDENTICON_CACHE", "true")
AVATAR_IDENTICON_SIZE = os.environ.get("AVATAR_IDENTICON_SIZE", "5")
AVATAR_IDENTICON_FOREGROUND = os.environ.get(
    "AVATAR_IDENTICON_FOREGROUND",
    [
        "rgb(45,79,255)",
        "rgb(254,180,44)",
        "rgb(226,121,234)",
        "rgb(30,179,253)",
        "rgb(232,77,65)",
        "rgb(49,203,115)",
        "rgb(141,69,170)",
    ],
)
AVATAR_IDENTICON_BACKGROUND = os.environ.get(
    "AVATAR_IDENTICON_BACKGROUND", "rgb(255,255,255)"
)

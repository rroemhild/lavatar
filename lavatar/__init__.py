# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import atexit
import hashlib
import threading

from flask import Flask
from flask_redis import Redis
from flask_ldapconn import LDAPConn


app = Flask('lavatar')
app.config.from_object('lavatar.default_settings')
app.config.from_envvar('LAVATAR_SETTINGS', silent=True)

redis_store = Redis(app)
ldap_conn = LDAPConn(app)


class User(ldap_conn.Entry):

    base_dn = app.config['LDAP_USER_BASEDN']
    object_class = app.config['LDAP_USER_OBJECTCLASS']

    mail = ldap_conn.Attribute(app.config['LDAP_USER_ATTR_MAIL'])
    photo = ldap_conn.Attribute(app.config['LDAP_USER_ATTR_PHOTO'])


# md5sum thread
def update_md5db_thread():
    search_filter = app.config.get('LDAP_USER_SEARCHFILTER', '')

    with app.app_context():
        users = User.query.filter(
            'mail: *, photo: *'
        ).filter(search_filter).all()

        for user in users:
            for mailaddr in user.mail:
                mail_md5 = hashlib.md5(mailaddr).hexdigest()
                if not redis_store.exists(mail_md5):
                    redis_store.setex(
                        mail_md5,
                        user.dn,
                        app.config['MD5DB_ENTRY_TTL']
                    )
                else:
                    redis_store.expire(
                        mail_md5,
                        app.config['MD5DB_ENTRY_TTL']
                    )

        app.logger.info('MD5db updated with %s entries from LDAP.',
                        len(users))


# init db on startup
update_md5db_thread()

# db update thread
md5dbThread = threading.Thread()
md5dbThread = threading.Timer(app.config['MD5DB_THREAD_TIMER'],
                              update_md5db_thread)
md5dbThread.start()
atexit.register(md5dbThread.cancel)

# Avatar Module
from lavatar.avatar import mod as avatarModule
app.register_blueprint(avatarModule)

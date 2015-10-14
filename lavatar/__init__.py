# -*- coding: utf-8 -*-

import atexit
import threading

from md5 import md5
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
    app.logger.info('Update md5db.')
    search_filter = app.config.get('LDAP_USER_SEARCHFILTER', '')

    with app.app_context():
        users = User.query.filter(
            'mail: *, photo: *'
        ).filter(search_filter).all()
        for user in users:
            for mailaddr in user.mail:
                md5sum = md5(mailaddr).hexdigest()
                if not redis_store.get(md5sum):
                    redis_store.setex(
                        md5sum,
                        mailaddr,
                        app.config['MD5DB_ENTRY_TTL']
                    )

        app.logger.debug('%s entries from LDAP.', len(users))


# init db on startup
update_md5db_thread()

# db update thread
md5dbThread = threading.Thread()
md5dbThread = threading.Timer(app.config['MD5DB_THREAD_TIMER'],
                              update_md5db_thread, ())
md5dbThread.start()
atexit.register(md5dbThread.cancel())

# Avatar Module
from lavatar.avatar import mod as avatarModule
app.register_blueprint(avatarModule)

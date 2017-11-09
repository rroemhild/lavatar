# -*- coding: utf-8 -*-

import hashlib
import logging
import threading

from six import text_type
from flask import Flask
from flask_redis import FlaskRedis
from flask_ldapconn import LDAPConn


app = Flask('lavatar')
app.config.from_object('lavatar.default_settings')
app.config.from_envvar('LAVATAR_SETTINGS', silent=True)

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

redis_store = FlaskRedis(app)
ldap_conn = LDAPConn(app)


class User(ldap_conn.Entry):

    base_dn = app.config['LDAP_USER_BASEDN']
    object_class = app.config['LDAP_USER_OBJECTCLASS']

    mail = ldap_conn.Attribute(app.config['LDAP_USER_ATTR_MAIL'])
    photo = ldap_conn.Attribute(app.config['LDAP_USER_ATTR_PHOTO'])


# md5sum thread
def update_md5db_thread():
    app.logger.info('Update MD5 Database.')
    search_filter = app.config.get('LDAP_USER_SEARCHFILTER', '')

    with app.app_context():
        users = User.query.filter(
            'mail: *, photo: *'
        ).filter(search_filter).all()

        for user in users:
            mailaddresses = user.mail
            if isinstance(mailaddresses, text_type):
                mailaddresses = [mailaddresses]

            for mailaddr in mailaddresses:
                ttl = int(app.config['MD5DB_ENTRY_TTL'])
                mail_md5 = hashlib.md5(mailaddr.encode('utf-8')).hexdigest()
                if not redis_store.exists(mail_md5):
                    redis_store.set(mail_md5, user.dn)
                    redis_store.expire(mail_md5, ttl)
                else:
                    redis_store.expire(mail_md5, ttl)

        app.logger.info('Found %s people entries in LDAP - updated Redis.',
                        len(users))

    threading.Timer(app.config['MD5DB_THREAD_TIMER'],
                    update_md5db_thread).start()


# init db updater
update_md5db_thread()

# Avatar Module
from lavatar.avatar import mod as avatarModule
app.register_blueprint(avatarModule)

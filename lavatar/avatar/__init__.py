# -*- coding: utf-8 -*-

import os
import hashlib
import mimetypes

from StringIO import StringIO
from flask import Blueprint, current_app, send_file, request, abort, url_for

from PIL import Image
from resizeimage import resizeimage
from pydenticon import Generator

from lavatar import redis_store, User

mod = Blueprint('avatar', __name__, url_prefix='/avatar')


RESIZE_METHODS = ['crop', 'cover', 'contain', 'width', 'height',
                  'thumbnail']


def _get_image_from_redis(dn_sha1hex, size='raw'):
    image = redis_store.hget(dn_sha1hex, size)
    return Image.open(StringIO(image))


def _get_image_from_ldap(user_dn, dn_sha1hex):
    try:
        user = User.query.get(user_dn)
        return user.photo
    except (IndexError, AttributeError, TypeError):
        return None


def _get_argval_from_request(match_args, default):
    match_args = set(match_args)
    request_args = set(request.args)

    try:
        arg = match_args.intersection(request_args).pop()
        retval = request.args.get(arg, default)
    except KeyError:
        retval = default

    return retval


def _max_size(size):
    max_size = int(current_app.config['AVATAR_MAX_SIZE'])
    default_size = int(current_app.config['AVATAR_DEFAULT_SIZE'])

    try:
        size = int(size)
        if size > max_size:
            size = max_size
    except ValueError:
        size = default_size

    return size


@mod.route('/<md5>', methods=['GET'])
def get_avatar(md5):
    image = None

    # fetch image from redis or ldap
    if redis_store.exists(md5):
        user_dn = redis_store.get(md5)
        dn_sha1hex = hashlib.sha1(user_dn).hexdigest()

        if redis_store.exists(dn_sha1hex):
            image = _get_image_from_redis(dn_sha1hex)
        else:
            image = _get_image_from_ldap(user_dn, dn_sha1hex)

            # cache image on redis
            if current_app.config.get('AVATAR_CACHE', True):
                img_ttl = current_app.config['AVATAR_TTL']
                redis_store.hset(dn_sha1hex, 'raw', str(image))
                redis_store.expire(dn_sha1hex, img_ttl)

            image = Image.open(StringIO(image))
    else:
        current_app.logger.warning('MD5 {0} not in redis.'.format(md5))

    # default image
    if image is None:
        default_args = ['d', 'default']
        default_image = current_app.config['AVATAR_DEFAULT_IMAGE']
        keyword = _get_argval_from_request(default_args, default_image)
        static_images = current_app.config['AVATAR_STATIC_IMAGES']
        static_path = current_app.config['AVATAR_STATIC']
        identicon_enable = current_app.config['AVATAR_IDENTICON_ENABLE']
        identicon_cache = current_app.config['AVATAR_IDENTICON_CACHE']

        if identicon_enable == 'true' and keyword == 'identicon':
            redis_key = md5 + "-identicon"

            # fetch image from redis
            if identicon_cache == 'true' and redis_store.exists(redis_key):
                image = _get_image_from_redis(redis_key)
            else:
                generator = Generator(int(current_app.config['AVATAR_IDENTICON_SIZE']),
                        int(current_app.config['AVATAR_IDENTICON_SIZE']),
                        foreground=current_app.config['AVATAR_IDENTICON_FOREGROUND'],
                        background=current_app.config['AVATAR_IDENTICON_BACKGROUND'])
                image = generator.generate(md5,
                        int(current_app.config['AVATAR_MAX_SIZE']),
                        int(current_app.config['AVATAR_MAX_SIZE']),
                        padding=(0,-4,0,-4))

                # cache image on redis
                if identicon_cache == 'true':
                    img_ttl = current_app.config['AVATAR_TTL']
                    redis_store.hset(redis_key, 'raw', str(image))
                    redis_store.expire(redis_key, img_ttl)

                image = Image.open(StringIO(image))

        elif keyword not in static_images or keyword == '404':
            abort(404)
        else:
            image = Image.open(
                os.path.join(static_path, static_images[keyword])
            )

    # sizes
    default_size = int(current_app.config['AVATAR_DEFAULT_SIZE'])
    size = _get_argval_from_request(['s', 'size'], default_size)
    width = _get_argval_from_request(['w', 'width'], default_size)
    height = _get_argval_from_request(['h', 'height'], default_size)

    # resize methods
    default_method = current_app.config['AVATAR_DEFAULT_METHOD']
    resize_method = _get_argval_from_request(['m', 'method'], default_method)
    if resize_method not in RESIZE_METHODS:
        resize_method = default_method

    if width == default_size and size != default_size:
        width = size
    if height == default_size and size != default_size:
        height = size

    if resize_method in ['crop', 'cover', 'contain', 'thumbnail']:
        size = (_max_size(width), _max_size(height))
    elif resize_method == 'width':
        size = _max_size(width)
    elif resize_method == 'height':
        size = _max_size(height)

    buffer_image = StringIO()

    try:
        resized_image = resizeimage.resize(resize_method, image, size)
    except resizeimage.ImageSizeError:
        if resize_method in ['width', 'height']:
            resized_image = image
        else:
            size = image.height if image.height > image.width else image.width
            size = (size, size)
            resized_image = resizeimage.resize(resize_method, image, size)

    resized_image.save(buffer_image, image.format, quality=95)
    buffer_image.seek(0)

    mimetypes.init()
    mimetype = mimetypes.types_map['.' + image.format.lower()]
    return send_file(buffer_image, mimetype=mimetype)

# -*- coding: utf-8 -*-

import os
import hashlib

from StringIO import StringIO
from flask import Blueprint, current_app, send_file, request, abort, url_for

from PIL import Image
from lavatar import redis_store, User

mod = Blueprint('avatar', __name__, url_prefix='/avatar')


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


def resize_and_crop(img, size):
    """Resize and crop an image to fit the specified size.

    Slightly modified version from https://gist.github.com/sigilioso/2957026

    args:
        img_path: image object.
        size: `(width, height)` tuple.
    raises:
        Exception: if can not open the file in img_path of there is problems
            to save the image.
        ValueError: if an invalid `crop_type` is provided.
    """
    crop_type = current_app.config.get('AVATAR_CROP_TYPE', 'top')
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    # The image is scaled/cropped vertically or horizontally depending on
    # the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], size[0] * img.size[1] / img.size[0]),
                         Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, (img.size[1] - size[1]) / 2, img.size[0],
                   (img.size[1] + size[1]) / 2)
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((size[1] * img.size[0] / img.size[1], size[1]),
                         Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if crop_type == 'top':
            box = (0, 0, size[0], img.size[1])
        elif crop_type == 'middle':
            box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2,
                   img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else:
            raise ValueError('ERROR: invalid value for crop_type')
        img = img.crop(box)
    else:
        img = img.resize((size[0], size[1]), Image.ANTIALIAS)
        # If the scale is the same, we do not need to crop
    return img


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

        if keyword not in static_images or keyword == '404':
            abort(404)

        image = Image.open(
            url_for('static',
                    filename=os.path.join('img', static_images[keyword]))
        )

    # size
    size_args = ['s', 'size']
    max_size = current_app.config['AVATAR_MAX_SIZE']
    default_size = int(current_app.config['AVATAR_DEFAULT_SIZE'])

    try:
        size = int(_get_argval_from_request(size_args, default_size))
        if size > max_size:
            size = max_size
    except ValueError:
        size = default_size

    buffer_image = StringIO()
    resized_image = resize_and_crop(image, (size, size))
    resized_image.save(buffer_image, 'JPEG', quality=90)
    buffer_image.seek(0)

    return send_file(buffer_image, mimetype='image/jpeg')

from http import HTTPStatus

from flask import Response
from flask import jsonify
from flask import request
from werkzeug.exceptions import HTTPException

from avdc.utility import image
from avdc.utility.misc import extractYear
from server import api
from server import app
from server.database import sqlite_db_init


@app.before_first_request
def _init_database():
    sqlite_db_init(app.config.get('DATABASE'))


@app.errorhandler(Exception)
def _return_json_if_error_occurred(e):
    if isinstance(e, HTTPException):
        status_code = e.code
    else:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        # log exception detail
        app.log_exception(e)

    # JSON response
    return jsonify(status=False,
                   message=str(e)), status_code


@app.route('/')
def _index():
    return jsonify(status=True, message='AVDC')


@app.route('/people/<name>')
def _people(name: str):
    images = api.GetPeopleByName(name)
    if not images:
        return jsonify(status=False,
                       message=f'people not found: {name}'), HTTPStatus.NOT_FOUND
    return jsonify(images)


@app.route('/image/people/<name>')
@app.route('/image/people/<name>/<int:index>')
def _people_image(name: str, index: int = 0):
    images = api.GetPeopleByName(name)
    if not images:
        return jsonify(status=False,
                       message=f'people image not found: {name}'), HTTPStatus.NOT_FOUND

    try:
        url = images[index]
    except IndexError:
        return jsonify(status=False,
                       message=f'index out of range: {index}: {name}'), HTTPStatus.NOT_FOUND

    data = image.imageToBytes(
        image.autoCropImage(
            image.bytesToImage(
                image.getRawImageByURL(url))))
    return Response(data, mimetype=f'image/jpeg')


@app.route('/metadata/<vid>')
@api.extract_vid
def _metadata(vid: str, c: bool):
    update = api.str_to_bool(
        request.args.get('update'))

    m = api.GetMetadataByVID(vid, update=update)
    if not m:
        return jsonify(status=False,
                       message=f'metadata not found: {vid}'), HTTPStatus.NOT_FOUND

    if c:  # add chinese subtitle tag
        m.tags.append('中文字幕')

    return jsonify(**m.toDict(),
                   year=extractYear(m.release))


@app.route('/image/backdrop/<vid>')
@api.extract_vid
def _backdrop_image(vid: str, _: bool):
    result = api.GetBackdropImageByVID(vid)
    if not result:
        return jsonify(status=False,
                       message=f'backdrop image not found: {vid}'), HTTPStatus.NOT_FOUND
    fmt, data = result
    return Response(data, mimetype=f'image/{fmt}')


@app.route('/image/primary/<vid>')
@api.extract_vid
def _primary_image(vid: str, _: bool):
    # dynamic generate primary image
    data = api.GetPrimaryImageByVID(vid)
    if not data:
        return jsonify(status=False,
                       message=f'primary image not found: {vid}'), HTTPStatus.NOT_FOUND
    return Response(data, mimetype=f'image/jpeg')

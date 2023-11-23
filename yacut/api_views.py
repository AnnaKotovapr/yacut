from flask import jsonify, request
from http import HTTPStatus

from . import app, db
from .error_handlers import InvalidAPIUsage
from .forms import is_correct
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify(url=url.original), 200


@app.route('/api/id/', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    
    short_id = data.get('custom_id', get_unique_short_id())
    
    if 'custom_id' not in data or data['custom_id'] is None or data['custom_id'] == '':
        short_id = get_unique_short_id()
    if URLMap.query.filter_by(short=short_id).first() is not None:
        raise InvalidAPIUsage(
            f'Предложенный вариант короткой ссылки уже существует.'
        )
    if len(short_id) > 16:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки', 
            HTTPStatus.BAD_REQUEST
        )
    if is_correct(short_id):
        url_map = URLMap()
        data['original'] = data['url']
        data['short'] = short_id
        url_map.from_dict(data)
        db.session.add(url_map)
        db.session.commit()
        response_data = {
            'short_link': f'http://localhost/{url_map.short}',
            'url': url_map.original
        }
        response_status = HTTPStatus.CREATED
        return jsonify(response_data), response_status
    else:
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки', 
            HTTPStatus.BAD_REQUEST
        )

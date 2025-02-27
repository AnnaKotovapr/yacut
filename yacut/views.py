from random import randint, choice
from string import hexdigits

from flask import flash, redirect, render_template

from . import app, db
from .forms import URL_mapForm
from .models import URLMap
from .constants import LINK_LENGTH, USER_INPUT_LIMIT


def get_unique_short_id():
    id_length = randint(LINK_LENGTH, LINK_LENGTH)
    unique_short_id = ''.join(choice(hexdigits) for _ in range(id_length))

    if URLMap.query.filter_by(short=unique_short_id).first():
        return get_unique_short_id()
    return unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm()
    if form.validate_on_submit():
        short_name = form.custom_id.data
        if URLMap.query.filter_by(short=short_name).first():
            flash(f'Имя {short_name} уже занято!')
            form.custom_id.data = None
            return render_template('index.html', form=form)
        if short_name is None or short_name == '':
            form.custom_id.data = get_unique_short_id()
        if len(form.custom_id.data) > USER_INPUT_LIMIT:
            flash('Указано недопустимое имя для короткой ссылки')
            form.custom_id.data = None
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
        db.session.add(url_map)
        db.session.commit()
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirection_view(short):
    map = URLMap.query.filter_by(short=short).first_or_404()
    if map is not None:
        original_link = map.original
        return redirect(original_link)

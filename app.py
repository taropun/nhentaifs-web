#!/usr/bin/python3

import os
import os.path
import sys

from bottle import abort, redirect, request, route, run, static_file, template


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = '{}/static'.format(SCRIPT_DIR)
NAVIGATION_SIZE = 7
ROW_COUNT = 5


def fs_path(path, *args):
    return os.path.join(sys.argv[1], path.format(*args))


@route('/static/<path:path>')
def serve_static(path):
    return static_file(path, root=STATIC_DIR)


@route('/img/<path:path>')
def serve_image(path):
    response = static_file(path, root=sys.argv[1])
    response.headers.pop('Content-Length')
    return response


@route('/')
def index():
    return template('index.html.tpl')


def window(index, width, items):
    if len(items) <= width:
        return items
    left_width = int(width / 2.0) + 1
    right_width = width - left_width
    start = max(0, index - left_width)
    end = min(len(items), index + right_width)
    actual_width = end - start
    if (index - start) < left_width:
        end += width - actual_width
    if (end - index) < right_width:
        start -= width - actual_width
    return items[start:end]


def chunks(items, count):
    for i in range(0, len(items), count):
        yield items[i:i + count]


def make_nav(page, count):
    return {
        'first': 1 if page > 1 else None,
        'previous': page - 1 if page > 1 else None,
        'next': page + 1 if page < count else None,
        'last': count if page < count else None,
        'window': window(page, NAVIGATION_SIZE, list(range(1, count + 1))),
        'current': page
    }


def fs_content(path, *args):
    with open(fs_path(path, *args), 'r') as f:
        return f.read()


def results_metadata(base):
    num_pages = int(fs_content('{}/num_pages', base))
    per_page = int(fs_content('{}/per_page', base))
    galleries = []
    for i in range(per_page):
        try:
            ID = fs_content('{}/{}/id', base, i)
        except FileNotFoundError:
            break
        title = fs_content('{}/{}/title/pretty', base, i)
        files = os.listdir(fs_path('{}/{}', base, i))
        thumb = ['{}/{}/{}'.format(base, i, f) for f in files
                 if f.startswith('thumb.')][0]
        galleries.append({'id': ID, 'title': title, 'thumb': thumb})
    return {'num_pages': num_pages, 'galleries': galleries}


@route('/all')
def frontpage():
    title = 'Frontpage'
    page = int(request.query.page or '1')
    metadata = results_metadata('all/{}'.format(page))
    num_pages = metadata['num_pages']
    galleries = chunks(metadata['galleries'], ROW_COUNT)
    nav = make_nav(page, num_pages)
    base = '/all?page='
    return template('results.html.tpl', title=title, base=base,
                    galleries=galleries, nav=nav)


@route('/search')
def search():
    query = request.query.query
    if not query:
        redirect('/all')
    title = 'Search: {}'.format(query)
    page = int(request.query.page or '1')
    metadata = results_metadata('search/{}/{}'.format(query, page))
    num_pages = metadata['num_pages']
    galleries = chunks(metadata['galleries'], ROW_COUNT)
    nav = make_nav(page, num_pages)
    base = '/search?query={}&page='.format(query)
    return template('results.html.tpl', title=title, base=base,
                    galleries=galleries, nav=nav)


@route('/tagged/<tag_id:int>')
def tagged(tag_id):
    title = 'Tag: {}'.format(tag_id)
    page = int(request.query.page or '1')
    metadata = results_metadata('tagged/{}/{}'.format(tag_id, page))
    num_pages = metadata['num_pages']
    galleries = chunks(metadata['galleries'], ROW_COUNT)
    nav = make_nav(page, num_pages)
    base = '/tagged/{}?page='.format(tag_id)
    return template('results.html.tpl', title=title, base=base,
                    galleries=galleries, nav=nav)


def group_tags(tags):
    result = {}
    for ID, tag in tags.items():
        key, value = tag.split(':')
        if key not in result:
            result[key] = {}
        result[key][ID] = value
    return result


def gallery_metadata(gallery_id):
    base = 'gallery/{}'.format(gallery_id)
    files = os.listdir(fs_path(base))
    tags = {ID: fs_content('{}/tags/{}', base, ID)
            for ID in os.listdir(fs_path('{}/tags', base))}
    return {
        'id': gallery_id,
        'title': {
            'pretty': fs_content('{}/title/pretty', base),
            'native': fs_content('{}/title/native', base),
            'english': fs_content('{}/title/english', base)
        },
        'cover': ['{}/{}'.format(base, f) for f in files
                  if f.startswith('cover.')][0],
        'tags': group_tags(tags),
        'filenames': fs_content('{}/filenames', base).split('\n'),
        'num_pages': int(fs_content('{}/num_pages', base)),
        'uploaded': int(fs_content('{}/uploaded', base))
    }


def related_metadata(gallery_id):
    base = 'related/{}'.format(gallery_id)
    directories = os.listdir(fs_path(base))
    galleries = []
    for directory in directories:
        base = 'related/{}/{}'.format(gallery_id, directory)
        files = os.listdir(fs_path(base))
        ID = fs_content('{}/id', base, directory)
        gallery = {
            'id': ID,
            'title': fs_content('{}/title/pretty', base),
            'cover': ['gallery/{}/{}'.format(ID, f) for f in files
                      if f.startswith('cover.')][0],
            'num_pages': fs_content('{}/num_pages', base)
        }
        galleries.append(gallery)
    return galleries


@route('/gallery/<gallery_id:int>')
def gallery(gallery_id):
    metadata = gallery_metadata(gallery_id)
    title = metadata['title']['pretty']
    filenames = ['/img/gallery/{}/thumbs/{}'.format(gallery_id, f)
                 for f in metadata['filenames']]
    thumbs = chunks(list(enumerate(filenames)), ROW_COUNT)
    related = related_metadata(gallery_id)
    return template('gallery.html.tpl', title=title,
                    thumbs=thumbs, metadata=metadata, related=related)


@route('/gallery/<gallery_id:int>/<page:int>')
def gallery_page(gallery_id, page):
    index = page - 1
    base = 'gallery/{}'.format(gallery_id)
    title = fs_content('{}/title/pretty', base)
    num_pages = int(fs_content('{}/num_pages', base))
    if page < 1 or page > num_pages:
        abort(404)
    nav = make_nav(page, num_pages)
    filenames = fs_content('{}/filenames', base).split('\n')
    page_url = '/img/gallery/{}/pages/{}'.format(gallery_id, filenames[index])
    base = '/gallery/{}/'.format(gallery_id)
    gallery_url = '/gallery/{}'.format(gallery_id)
    return template('gallery_page.html.tpl', title=title, base=base,
                    nav=nav, page_url=page_url, gallery_url=gallery_url)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <mountpoint>'.format(sys.argv[0]))
        sys.exit(1)
    try:
        port = int(os.getenv('PORT') or '8080')
        run(port=port)
    except FileNotFoundError:
        abort(404)

# TODO:

# app:
# - [ ] settings page with strict cookies

# CSS:
# - [ ] make it dark
# - [ ] highlight large galleries

# JS:
# - [ ] load thumbs as they scroll into view
# - [ ] preload gallery images relative to the current one
# - [ ] bind keys in gallery viewer

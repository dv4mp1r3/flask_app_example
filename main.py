from flask import Flask, request, render_template
import requests
import json

elasticRecordLimit = 10
elasticRecordCount = 0
el_url = 'http://localhost:9200/data/doc'

appName = 'random_app'
app = Flask(appName)


def search(query, page):
    global elasticRecordCount
    global elasticRecordLimit
    result = None
    offset = (page - 1) * elasticRecordLimit
    el_query = {
        "query": {
            "match": {"text": query}
        }
    }
    try:
        response = json.loads(requests.post(el_url+'/_count', json=el_query).text)
        elasticRecordCount = int(response['count'])
        if elasticRecordCount > 0:
            el_query['from'] = offset
            el_query['size'] = elasticRecordLimit
            response = requests.post(el_url+'/_search', json=el_query)
            result = json.loads(response.text)
            result = result['hits']['hits']
    except Exception:
        return None
    return result


def filter_page(page):
    if page is not None:
        page = int(page)
        if page is 0 or page < 0:
            page = 1
    return page


@app.route("/")
def main():
    query = get_get('query')
    data = None
    page = None
    if query is not None:
        page = filter_page(get_get('page'))
        data = search(query, page)
        title = appName + ': searching for ' + query
    else:
        title = appName + ': main page'
    return render_template("main.html",
                           title=title,
                           query=query,
                           result=data,
                           pagination=prepare_pagination(page))


def prepare_pagination(page):
    '''
    Тест 1: страниц больше 9 + (первая, последняя, переход по страницам)
    Тест 2: страниц меньше 9 но больше 1 +
    Тест 3: одна страница +

    Генерация массива для вывода пагинации
    :param page: номер страницы, на которую переходит пользователь
    :param record_count: количество всего записей по текущему запросу
    :return:
    '''
    global elasticRecordCount
    global elasticRecordLimit
    result = []
    if elasticRecordCount <= 0:
        return None
    pages_max_limit = 9
    max_pages = int(elasticRecordCount / elasticRecordLimit)

    pagination = {
        'limit': elasticRecordLimit,
        'max': max_pages,
        'current': page,
        'pages': {},
    }

    # расчет максимального количества страниц
    if max_pages is 1:
        return pagination
    elif max_pages < pages_max_limit:
        pages_max_limit = max_pages

    # при невалидном значении страницы выставляется 1
    if page > max_pages:
        page = 1

    mid = int(pages_max_limit / 2)
    min_page = page - mid
    max_page = page + mid
    if min_page <= 0:
        min_page = 1
        max_page = pages_max_limit
    elif max_page >= max_pages:
        max_page = max_pages
        min_page = max_page - pages_max_limit

    i = min_page
    result.append({
        'number': 1,
        'class': 'prev',
        'caption': '«'
    })

    while True:
        cl = ''
        tmp = i
        if tmp is page:
            cl = 'active'
        result.append({
            'number': tmp,
            'class': cl,
            'caption': tmp
        })
        if i is max_page:
            break
        i = i + 1
    result.append({
        'number': max_pages,
        'class': 'next',
        'caption': '»'
    })
    pagination['pages'] = result

    return pagination


def get_post(param):
    return request.values.get(param) or None


def get_get(param):
    return request.values.get(param) or None


@app.route("/account/<username>/")
def account(username):
    title = appName + ': Account ' + username + ' not found'
    username = username or None
    if username is None:
        return render_template("404.html",
                               name='username',
                               value=username,
                               title=title)
    title = appName + 'Account details'
    return render_template("account.html", username=username, title=title)

#tests
#search('version number', 1)
#prepare_pagination(81)

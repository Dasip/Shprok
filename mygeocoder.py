# coding:utf-8

import requests

def geocode(address):
    # Собираем запрос для геокодера.
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={0}&format=json".format(address)
    
    # Выполняем запрос.
    response = requests.get(geocoder_request)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
            request=g_request, status=response.status_code, reason=response.reason))

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return toponym[0]["GeoObject"] if toponym else None


# Получаем координаты объекта по его адресу.
def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return (None,None)
    
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Широта, преобразованная в плавающее число:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_spn(address):
    toponym = geocode(address)
    if not toponym:
        return (None, None)
    # долгота, широта
    # longitude latitude
    toponym_coords = toponym['Point']['pos']
    ll = ','.join(toponym_coords.split(' '))
    # рамка
    envelope = toponym['boundedBy']['Envelope']
    xright, ybot = envelope['lowerCorner'].split(' ')
    xleft, ytop = envelope['upperCorner'].split(' ')
    spx = str(abs(float(xleft) - float(xright)))
    spy = str(abs(float(ybot) - float(ytop)))
    spn = '{},{}'.format(spx, spy)
    return (ll, spn)


def corporation_finder(ll, spn, type_request, locale='ru_RU'):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    search_params = {
        "apikey": api_key,
        "text": type_request,
        "lang": locale,
        "ll": ll,
        'spn': spn,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
            request=g_request, status=response.status_code, reason=response.reason))

    # Получаем первую найденную организацию
    corpa = json_response['features'][0]['properties']['CompanyMetaData']['address']
    return corpa if corpa else None
 
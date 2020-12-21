import json
from os import environ
from datetime import datetime, timezone
import requests
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)


def get_user_location():
    '''Get the user's current location'''

    if 'X-Forwarded-For' in request.headers:
        ip_address = str(request.headers['X-Forwarded-For'])
        method = 'x-forwarded'
    else:
        ip_address = str(request.environ.get('HTTP_X_REAL_IP',
                         request.remote_addr))
        method = 'http-x-real-ip'

    if ip_address == '127.0.0.1':
        ip_address = requests.get('http://ipecho.net/plain').text
        method = '127.0.0.1 used'

    # url = f'http://ip-api.com/json/{ip_address}'
    # response = requests.get(url)
    # text = response.json()

    # if text['status'] == 'success':
    #     lat = text['lat']
    #     lon = text['lon']
    #     region_name = text['regionName']
    #     city = text['city']
    #     country = text['country']
    #     return passing, lat, lon, region_name, city, country
    # else:
    #     return text, passing
    return method, ip_address


def get_geographic_location(ip_addr):
    '''Get latitude and longitude'''

    api_key = environ.get('IPGEO_API_KEY')

    url = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_addr}&fields=geo')

    if url.status_code == 200:
        data = url.text
        info = json.loads(data)
        json.dumps(info, ensure_ascii=False)
        return info
    return None


@main.route('/', methods=['GET', 'POST'])
def index():
    '''Index route'''

    user_agent = request.headers.get('User-Agent')
    host = request.headers.get('Host')
    referer = request.headers.get('Referer')

    ipaddress = get_user_location()
    method = ipaddress[0]
    ip_address = ipaddress[1]
    data = get_geographic_location(ip_address)
    lat = data['latitude']
    lon = data['longitude']
    now = datetime.now(tz=timezone.utc).strftime(
                          '%Y-%m-%d %H:%M:%S:%f %Z%z')
    content = {
            'user_agent': user_agent,
            'host': host,
            'referer': referer,
            'method': method,
            'ip_address': ip_address,
            'lat': lat,
            'lon': lon,
            'now': now
            }
    return render_template('main/index.html', **content)


@main.app_errorhandler(404)
def page_not_found(error):
    '''Page not found'''

    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    '''Internal server error'''

    return render_template('500.html'), 500

import json
from os import environ
from datetime import datetime, timezone
import requests
from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)


def get_user_ip_address():
    '''Get the user's IP address'''

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

    return method, ip_address


def get_geo_location(ip_addr):
    '''Get latitude and longitude from IP address'''

    api_key = environ.get('IPGEO_API_KEY')

    url = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey'
                       f'={api_key}&ip={ip_addr}&fields=geo&excludes=ip')

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

    ipaddress = get_user_ip_address()
    method = ipaddress[0]
    ip_address = ipaddress[1]
    data = get_geo_location(ip_address)
    lat = data['latitude']
    lon = data['longitude']
    country_code2 = data['country_code2']
    country_name = data['country_name']
    state_prov = data['state_prov']
    district = data['district']
    city = data['city']
    zipcode = ['zipcode']
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
            'country_code2': country_code2,
            'country_name': country_name,
            'state_prov': state_prov,
            'district': district,
            'city': city,
            'zipcode': zipcode,
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

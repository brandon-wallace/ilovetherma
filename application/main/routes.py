from datetime import datetime, timezone
import requests
from flask import (Blueprint, render_template, url_for, redirect, request)

main = Blueprint('main', __name__)


def get_user_location():
    '''Get the user's current location'''

    method = ''

    if 'X-Forwarded-For' in request.headers:
        ip_address = request.headers['X-Forwarded-For']
        method = 'x-forwarded'
    else:
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
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


@main.route('/', methods=['GET', 'POST'])
def index():
    '''Index route'''

    user_agent = request.headers.get('User-Agent')
    host = request.headers.get('Host')
    referer = request.headers.get('Referer')

    location = get_user_location()
    method = location[0]
    ip_address = location[1]
    now = datetime.now(tz=timezone.utc).strftime(
                          '%Y-%m-%d %H:%M:%S:%f %Z%z')
    content = {
            'location': location,
            'method': method,
            'ip_address': ip_address,
            'now': now,
            'user_agent': user_agent,
            'host': host,
            'referer': referer
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

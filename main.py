from datetime import datetime
import os
import json

from flask import (
    request,
    send_file,
    abort,
    Flask
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from git.cmd import Git


if not os.path.exists("secrets.json"):
    print("CRITICAL: secrets.json not found, cannot start server")
    exit()

with open("secrets.json", "rb") as f:
    secrets = json.load(f)

main = Flask(__name__)

main.config['SECRET_KEY'] = secrets['secretKey']

del secrets

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['10/second']
)
limiter.init_app(main)


########################################################################
########################################################################
#######################       Endpoints        #########################
########################################################################
########################################################################


@main.route('/CDN/images/<image_name>')
def images(image_name: str):
    """
    Send the requested image file if it exists.

    Args:
    image_name: The name of the requested image file.

    Returns:
    Send file: The requested image file if it exists.
    """
    
    if image_name not in os.listdir('CDN//images'):
        abort(404)
    
    return send_file(f'CDN//images//{image_name}')


########################################################################
########################################################################
#######################       Errors        ############################
########################################################################
########################################################################


@main.before_first_request
def clean_up_on_startup():
    with open("secrets.json", "rb") as f:
        secrets = json.load(f)
    if secrets['dev'] == False:
        os.system('git reset --hard HEAD')
        repopull = Git().pull('https://github.com/LukeNeedle/blog-cdn.git')
    if os.path.exists('LOGS/404.log'):
        os.remove('LOGS/404.log')
    if os.path.exists('LOGS/429.log'):
        os.remove('LOGS/429.log')

def handle_not_found(error):
    if not os.path.exists('LOGS/404.log'):
        open('LOGS/404.log', 'w')
    with open('LOGS/404.log', 'a') as f:
        f.write(str(datetime.now()) + ' | ' + str(request.remote_addr) + ' | ' + str(request.url) + '\n')
    return "", 404


def rate_limit_reached(error):
    if not os.path.exists('LOGS/429.log'):
        open('LOGS/429.log', 'w')
    with open('LOGS/429.log', 'a') as f:
        f.write(str(datetime.now()) + ' | ' + str(request.remote_addr) + ' | ' + str(request.url) + '\n')
    return "", 429


if __name__ == '__main__':
    if not os.path.exists('LOGS'):
        os.mkdir('LOGS')
    main.register_error_handler(429, rate_limit_reached)
    main.register_error_handler(404, handle_not_found)
    main.run(debug=True, host='0.0.0.0')

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

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets['secretKey']

del secrets

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['10/second']
)
limiter.init_app(app)


########################################################################
########################################################################
#######################       Endpoints        #########################
########################################################################
########################################################################


@app.route('/api/keepalive')
def keepalive_api():
    return "I'm Alive!"

@app.route('/CDN/images/<image_name>')
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


@app.before_first_request
def clean_up_on_startup():
    if not os.path.exists('LOGS'):
        os.mkdir('LOGS')
    with open("secrets.json", "rb") as f:
        secrets = json.load(f)
    if secrets['dev'] == False:
        os.system('git reset --hard HEAD')
        repopull = Git().pull('https://github.com/LukeNeedle/blog-cdn.git')
    if os.path.exists('LOGS/404.log'):
        os.remove('LOGS/404.log')
    if os.path.exists('LOGS/429.log'):
        os.remove('LOGS/429.log')

@app.errorhandler(404)
def handle_not_found(error):
    if not os.path.exists('LOGS/404.log'):
        open('LOGS/404.log', 'w')
    with open('LOGS/404.log', 'a') as f:
        f.write(str(datetime.now()) + ' | ' + str(request.remote_addr) + ' | ' + str(request.url) + '\n')
    return "Error: file not found", 404

@app.errorhandler(429)
def rate_limit_reached(error):
    if not os.path.exists('LOGS/429.log'):
        open('LOGS/429.log', 'w')
    with open('LOGS/429.log', 'a') as f:
        f.write(str(datetime.now()) + ' | ' + str(request.remote_addr) + ' | ' + str(request.url) + '\n')
    return "Error: rate limit reached", 429


if __name__ == '__main__':
    if not os.path.exists('LOGS'):
        os.mkdir('LOGS')
    app.register_error_handler(429, rate_limit_reached)
    app.register_error_handler(404, handle_not_found)
    app.run(debug=True, host='0.0.0.0')

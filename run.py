import logging
import os

from app import app

web_host = os.environ['HAPIDOC_WEB_HOST']
web_port = os.environ['HAPIDOC_WEB_PORT']


def start_app():
    app.run(host=web_host, port=web_port)


if __name__ == "__main__":
    logs_dir = 'logs'
    log_filename = os.path.join(logs_dir, 'hapidocweb.log')
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    start_app()

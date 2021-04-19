import os

APP_VERSION='v0.1'
APP_NAME = 'OSDG-tool'
APP_DOCS_URL = '/docs'
APP_DEBUG = True

SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = os.getenv('SERVER_PORT', 5000)
SERVER_LOG_LEVEL = os.getenv('SERVER_LOG_LEVEL', 'debug')

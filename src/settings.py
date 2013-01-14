# configuration
DEBUG = True
SECRET_KEY = 'development key'
MEDIA_DIR = 'media/'
MEDIA_URL = '/media'
PLAYER = "divx"
AUTOPLAY = "1"
TITLE = "El Jonathan"
VALID_EXTENSIONS = [ '.mpg', '.mpeg', '.ogg', '.ogm', '.ogv', '.divx', '.avi', '.webm', '.mkv', '.mov' ]
IGNORE_POINT_PATH = True
BASE_URL = "http://127.0.0.1:5000/"

try:
    from settings_local import *
except ImportError:
    pass

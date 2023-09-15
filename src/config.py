import os


DIR_SRC = os.path.dirname(__file__)
DIR_ROOT = os.path.join(DIR_SRC, '..')
DIR_DATA = os.path.join(DIR_ROOT, 'data')
DIR_DOC = os.path.join(DIR_ROOT, 'doc')

FILE_IMAGE_DEFAULT = os.path.join(DIR_DATA, 'no_photo.jpg')
FILE_IMAGE_LOGO = os.path.join(DIR_DATA, 'organizer_logo.png')
FILE_SECRETS = os.path.join(DIR_DATA, 'secrets.json')

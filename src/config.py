import os


DIR_SRC = os.path.dirname(__file__)
DIR_LANGUAGE = os.path.join(DIR_SRC, 'language')
DIR_ROOT = os.path.join(DIR_SRC, '..')
DIR_DATA = os.path.join(DIR_ROOT, 'data')
DIR_DOC = os.path.join(DIR_ROOT, 'doc')

FILE_IMAGE_DEFAULT = os.path.join(DIR_DATA, 'no_photo.jpg')
FILE_IMAGE_LOGO = os.path.join(DIR_DATA, 'organizer_logo.png')
FILE_IMAGE_FLAG_PL = os.path.join(DIR_DATA, 'flag_polish.jpg')
FILE_IMAGE_FLAG_ENG = os.path.join(DIR_DATA, 'flag_english.jpg')
FILE_SECRETS = os.path.join(DIR_DATA, 'secrets.json')

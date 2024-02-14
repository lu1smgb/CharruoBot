import dotenv
import os
import logging
from logging.config import dictConfig

dotenv.load_dotenv(override=True)

# Clave privada del bot, esencial para que funcione
# !!! NO COMPARTIR !!!
BOT_TOKEN : str = os.environ.get('BOT_TOKEN')

# ID de usuario de Proxx
PROXX_ID : str = os.environ.get('PROXX_ID')

# ID del servidor de Charruo
SERVER_ID : int = int(os.environ.get('SERVER_ID'))

# ID del servidor de pruebas
TEST_SERVER_ID : int = int(os.environ.get('TEST_SERVER_ID'))

# Configuracion acerca de la creacion de logs
LOGGING_CONFIG = {
    'version': 1,
    'disabled_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        'normal': {
            'format': "%(levelname)-10s - %(asctime)s : %(message)s"
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'normal'
        },
        'console2': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'normal'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': 'logs/infos.log',
            'mode': "w"
        }
    },
    'loggers': {
        'bot': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'discord': {
            'handlers': ['console2', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
dictConfig(LOGGING_CONFIG)
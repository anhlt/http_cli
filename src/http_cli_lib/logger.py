import logging
import os

current_path = os.path.dirname(os.path.abspath(__file__))

logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s: %(name)-2s: %(levelname)-8s %(message)s'}
    },
    handlers={
        'console': {'class': 'logging.StreamHandler',
                    'formatter': 'f',
                    'level': logging.DEBUG},
        'file': {'class': 'logging.FileHandler',
                 'formatter': 'f',
                 'level': logging.DEBUG,
                 'filename': os.path.join(current_path, 'debug.log')
                 }
    },
    root={
        'handlers': ['file'],
        'level': logging.DEBUG,
    },
)

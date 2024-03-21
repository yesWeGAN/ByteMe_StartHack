import logging
import logging.config

# Set up the configuration for logging
def get_logging_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
            },
        },
        'handlers': {
            'default': {
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'root': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }



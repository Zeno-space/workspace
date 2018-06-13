import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, 'db')
LOG_PATH = os.path.join(BASE_DIR, 'log')

LOG_LEVEL = {
    'base_level': logging.DEBUG,
    'operation.log': {
        'file': logging.INFO,
        'screan': logging.INFO
    },
    'consumption.log': {
        'file': logging.INFO,
        'screan': logging.INFO
    },
    'debug.log': {
        'file': logging.DEBUG,
        'screan': logging.DEBUG
    }
}

#---------------bank config-----------------
BANK_DB_PATH = os.path.join(DB_PATH, 'bank_db.json')

#------------shopping_cart config-----------
SC_DB_PATH = os.path.join(DB_PATH, 'sc_db.json')

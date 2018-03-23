import os

EQ_SCHEMA_VALIDATOR_URL = os.getenv('EQ_SCHEMA_VALIDATOR_URL')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', False)
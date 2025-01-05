import os
from pathlib import Path

from dotenv import dotenv_values

path_project = Path(__file__).resolve().parents[1]
env_values = dotenv_values(path_project/'.env')

# Chroma DB related constants
CHROMA_HOST = os.environ.get(
    'CHROMA_HOST', default=env_values.get('CHROMA_HOST'))
CHROMA_PORT = int(
    os.environ.get('CHROMA_PORT', default=env_values.get('CHROMA_PORT'))
)
CHROMA_SERVER_AUTHN_PROVIDER = os.environ.get(
    'CHROMA_SERVER_AUTHN_PROVIDER',
    default=env_values.get('CHROMA_SERVER_AUTHN_PROVIDER'))
CHROMA_CLIENT_AUTHN_PROVIDER = os.environ.get(
    'CHROMA_CLIENT_AUTHN_PROVIDER',
    default=env_values.get('CHROMA_CLIENT_AUTHN_PROVIDER'))
CHROMA_PASSWORD = os.environ.get(
    'CHROMA_PASSWORD', default=env_values.get('CHROMA_PASSWORD'))
CHROMA_SERVER_AUTHN_CREDENTIALS_FILE = os.environ.get(
    'CHROMA_SERVER_AUTHN_CREDENTIALS_FILE',
    default=env_values.get('CHROMA_SERVER_AUTHN_CREDENTIALS_FILE'))
CHROMA_USER = os.environ.get(
    'CHROMA_USER', default=env_values.get('CHROMA_USER'))

# Telegram bot
TELEGRAM_BOT_TOKEN = os.environ.get(
    'TELEGRAM_BOT_TOKEN',
    default=env_values.get('TELEGRAM_BOT_TOKEN')
)

# RAG vectorizer
EMBEDDING_MODEL_NAME = os.environ.get(
    'EMBEDDING_MODEL_NAME',
    default=env_values.get('EMBEDDING_MODEL_NAME'))
EMBEDDING_DIMENSION = int(
    os.environ.get('EMBEDDING_DIMENSION',
                   default=env_values.get('EMBEDDING_DIMENSION'))
)

# LLM constants for processing text
LLM_API_KEY = os.environ.get(
    'LLM_API_KEY', default=env_values.get('LLM_API_KEY'))
LLM_BASE_URL = os.environ.get(
    'LLM_BASE_URL', default=env_values.get('LLM_BASE_URL'))
if LLM_BASE_URL == "":
    LLM_BASE_URL = None
LLM_MODEL_NAME = os.environ.get(
    'LLM_MODEL_NAME', default=env_values.get('LLM_MODEL_NAME'))

# Path to data files
DATA_COMMENTS = os.environ.get(
    'DATA_COMMENTS', default=env_values.get('DATA_COMMENTS'))
DATA_RULES = os.environ.get(
    'DATA_RULES', default=env_values.get('DATA_RULES'))

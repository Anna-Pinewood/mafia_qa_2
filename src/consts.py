import os
from dotenv import dotenv_values
from pathlib import Path
path_project = Path(__file__).resolve().parents[1]
env_values = dotenv_values(path_project/'.env')

# Chroma DB related constants
CHROMA_HOST = os.environ.get(
    'CHROMA_HOST', default=env_values['CHROMA_HOST'])
CHROMA_PORT = int(
    os.environ.get('CHROMA_PORT', default=env_values['CHROMA_PORT'])
)
CHROMA_SERVER_AUTHN_PROVIDER = os.environ.get(
    'CHROMA_SERVER_AUTHN_PROVIDER', default=env_values['CHROMA_SERVER_AUTHN_PROVIDER'])
CHROMA_CLIENT_AUTHN_PROVIDER = os.environ.get(
    'CHROMA_CLIENT_AUTHN_PROVIDER', default=env_values['CHROMA_CLIENT_AUTHN_PROVIDER'])
CHROMA_PASSWORD = os.environ.get(
    'CHROMA_PASSWORD', default=env_values['CHROMA_PASSWORD'])
CHROMA_SERVER_AUTHN_CREDENTIALS_FILE = os.environ.get(
    'CHROMA_SERVER_AUTHN_CREDENTIALS_FILE', default=env_values['CHROMA_SERVER_AUTHN_CREDENTIALS_FILE'])
CHROMA_USER = os.environ.get(
    'CHROMA_USER', default=env_values['CHROMA_USER'])

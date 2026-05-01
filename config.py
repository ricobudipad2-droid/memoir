import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    DB_PATH = os.getenv('DATABASE_URL', 'memoir.db')
    MIMO_API_KEY = os.getenv('MIMO_API_KEY', '')
    MIMO_BASE_URL = os.getenv('MIMO_BASE_URL', 'https://api.mimo.xiaomi.com/v1')
    MIMO_MODEL = os.getenv('MIMO_MODEL', 'MiMo-v2.5')
    PORT = int(os.getenv('PORT', '8888'))

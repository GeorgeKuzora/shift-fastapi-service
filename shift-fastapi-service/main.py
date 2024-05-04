import auth.views as auth
import views
from dotenv import load_dotenv
from app import app
from logs import init_logging

load_dotenv()
init_logging()

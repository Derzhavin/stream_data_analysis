from app.infra.web import create_web_app
from app.infra.background import create_background_app

web_app = create_web_app()
background_app = create_background_app()
from app.base.api.factory import Factory
from config import apiConfig

factory = Factory()
app = factory.create_app(config=apiConfig)
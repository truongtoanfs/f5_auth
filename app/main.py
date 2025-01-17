import uvicorn

from app.base.api.factory import Factory
from config import apiConfig

factory = Factory()
app = factory.create_app(config=apiConfig)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

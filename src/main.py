import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
# from db import elastic, redis

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.post(
        "api/v1/ugc/events/watch",
        response_model=        
):
    # где-то будет Depends?
    pass

# 1. по ручке приходит json {"topic":'views', "value": b'1611039931', "key": b'500271+tt0120338'}
# 2. Есть проверка входных данных (pydantic, annotated)
# 3. Модель pydantic попадает в QueueSerailizerManagerб
# который берет нужный экземпляр класса QueueSerializer (WatchEventSerializer) и с помощью него получает бинарную строку, которую затем отправляет в клиент queue

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from routers.main import main_router
import settings


app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION,
              docs_url=settings.APP_DOCS_URL,
              debug=settings.APP_DEBUG)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'info': 'Something is wrong with the input data.',
                                  'meta': {'detail': exc.errors(),
                                           'body': exc.body}}))


def configure():
    app.include_router(main_router)


configure()
if __name__ == '__main__':
    uvicorn.run(app,
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                log_level=settings.SERVER_LOG_LEVEL)

from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import traceback

from core.fos.fos_extractor import FosExtractor
from core.sdg.sdg_tagger import SdgTagger


main_router = APIRouter()

fos_extractor = FosExtractor()
sdg_tagger = SdgTagger()


class TagInput(BaseModel):
    text: str
    detailed: Optional[bool] = False
    text_type: str = 'paragraph'
    submerge_fos: bool = False
    return_fos: Optional[bool] = False


class TagManyInput(BaseModel):
    texts: List[str]
    detailed: Optional[bool] = False
    text_type: str = 'paragraph'
    submerge_fos: bool = False
    return_fos: Optional[bool] = False


with open('templates/index.html', 'r') as file_:
    index_html = file_.read()


@main_router.get('/')
async def home():
    return HTMLResponse(content=index_html)


@main_router.post('/tag')
async def tag(item: TagInput):
    try:
        fos = fos_extractor.extract(item.text, text_type=item.text_type, submerge=item.submerge_fos)
        sdgs = sdg_tagger.tag(fos, detailed=item.detailed)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(ex), 'meta': traceback.format_exc(), 'status': 'ERROR'})
    if item.return_fos:
        result = {'fos': fos, 'sdgs': sdgs}
    else:
        result = sdgs
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'result': result, 'status': 'OK'})


@main_router.post('/tag_many')
async def tag_many(item: TagManyInput):
    foses, sdgs = list(), list()
    try:
        for text in item.texts:
            text_fos = fos_extractor.extract(text, text_type=item.text_type, submerge=item.submerge_fos)
            text_sdgs = sdg_tagger.tag(text_fos, detailed=item.detailed)
            if item.return_fos:
                foses.append(text_fos)
            sdgs.append(text_sdgs)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(ex), 'meta': traceback.format_exc(), 'status': 'ERROR'})

    result = {'sdgs': sdgs}
    if item.return_fos:
        result['foses'] = foses
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'result': result, 'status': 'OK'})
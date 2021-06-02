from typing import List, Optional

import requests
from pydantic import HttpUrl
from fastapi import APIRouter, Depends, File, UploadFile, Form
from instagrapi.types import (
    Story, StoryHashtag, StoryLink,
    StoryLocation, StoryMention, StorySticker
)

from helpers import photo_upload_story
from dependencies import ClientStorage, get_clients


router = APIRouter(
    prefix="/photo",
    tags=["photo"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload_to_story", response_model=Story)
async def photo_upload_to_story(sessionid: str = Form(...),
                                file: UploadFile = File(...),
                                caption: Optional[str] = Form(''),
                                mentions: List[StoryMention] = [],
                                locations: List[StoryLocation] = [],
                                links: List[StoryLink] = [],
                                hashtags: List[StoryHashtag] = [],
                                stickers: List[StorySticker] = [],
                                clients: ClientStorage = Depends(get_clients)
                                ) -> Story:
    """Upload photo to story
    """
    cl = clients.get(sessionid)
    content = await file.read()
    return await photo_upload_story(
        cl, content, caption,
        mentions=mentions,
        links=links,
        hashtags=hashtags,
        locations=locations,
        stickers=stickers
    )


@router.post("/upload_to_story/by_url", response_model=Story)
async def photo_upload_to_story_by_url(sessionid: str = Form(...),
                                url: HttpUrl = Form(...),
                                caption: Optional[str] = Form(''),
                                mentions: List[StoryMention] = [],
                                locations: List[StoryLocation] = [],
                                links: List[StoryLink] = [],
                                hashtags: List[StoryHashtag] = [],
                                stickers: List[StorySticker] = [],
                                clients: ClientStorage = Depends(get_clients)
                                ) -> Story:
    """Upload photo to story by URL to file
    """
    cl = clients.get(sessionid)
    content = requests.get(url).content
    return await photo_upload_story(
        cl, content, caption,
        mentions=mentions,
        links=links,
        hashtags=hashtags,
        locations=locations,
        stickers=stickers
    )

import datetime
import json
import logging

from aiohttp import web
from telethon.tl import types

from .config import chat_ids
from .util import get_file_name, get_human_size

log = logging.getLogger(__name__)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class Views:

    def __init__(self, client):
        self.client = client

    async def home(self, req):
        chats = []
        for chat in chat_ids:
            chats.append({
                'id': chat['alias_id'],
                'name': chat['title']
            })
        return web.json_response({'chats': chats})

    async def index(self, req):
        alias_id = req.rel_url.path.split('/')[1]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        log_msg = ''
        try:
            offset_val = int(req.query.get('page', '1'))
        except:
            offset_val = 1
        log_msg += f"page: {offset_val} | "
        try:
            search_query = req.query.get('search', '')
        except:
            search_query = ''
        log_msg += f"search query: {search_query} | "
        offset_val = 0 if offset_val <= 1 else offset_val - 1
        try:
            kwargs = {
                'entity': chat_id,
                'limit': 100,
                'add_offset': 100 * offset_val
            }
            if search_query:
                kwargs.update({'search': search_query})
            messages = (await self.client.get_messages(**kwargs)) or []

        except:
            log.debug("failed to get messages", exc_info=True)
            messages = []
        log_msg += f"found {len(messages)} results | "
        log.debug(log_msg)
        results = []
        for m in messages:
            entry = None
            if m.file and not isinstance(m.media, types.MessageMediaWebPage):
                entry = dict(
                    file_id=m.id,
                    media=True,
                    mime_type=m.file.mime_type,
                    insight=get_file_name(m)[:55],
                    date=m.date,
                    size=get_human_size(m.file.size),
                    url=req.rel_url.with_path(f"/{alias_id}/{m.id}/view")
                )

            if entry:
                results.append(entry)
        prev_page = False
        next_page = False
        if offset_val:
            query = {'page': offset_val}
            if search_query:
                query.update({'search': search_query})
            prev_page = {
                'url': req.rel_url.with_query(query),
                'no': offset_val
            }

        if len(messages) == 20:
            query = {'page': offset_val + 2}
            if search_query:
                query.update({'search': search_query})
            next_page = {
                'url': req.rel_url.with_query(query),
                'no': offset_val + 2
            }

        data = {
            'item_list': results,
            'prev_page': prev_page,
            'cur_page': offset_val + 1,
            'next_page': next_page,
            'search': search_query,
            'name': chat['title'],
            'logo': req.rel_url.with_path(f"/{alias_id}/logo")
        }

        dumps = json.dumps(data, default=myconverter)

        return web.json_response(json.loads(dumps))

    async def info(self, req):
        pass

    async def logo(self, req):
        alias_id = req.rel_url.path.split('/')[1]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        photo = await self.client.get_profile_photos(chat_id)
        if not photo:
            return web.Response(status=404, text="404: Chat has no profile photo")
        photo = photo[0]
        size = photo.sizes[0]
        media = types.InputPhotoFileLocation(
            id=photo.id,
            access_hash=photo.access_hash,
            file_reference=photo.file_reference,
            thumb_size=size.type
        )
        body = self.client.iter_download(media)
        r = web.Response(
            status=200,
            body=body,
        )
        r.enable_chunked_encoding()
        return r

    async def download_get(self, req):
        return await self.handle_request(req)

    async def download_head(self, req):
        return await self.handle_request(req, head=True)

    async def thumbnail_get(self, req):
        return await self.handle_request(req, thumb=True)

    async def thumbnail_head(self, req):
        return await self.handle_request(req, head=True, thumb=True)

    async def handle_request(self, req, head=False, thumb=False):
        file_id = int(req.match_info["id"])
        alias_id = req.rel_url.path.split('/')[1]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        message = await self.client.get_messages(entity=chat_id, ids=file_id)
        if not message or not message.file:
            log.debug(f"no result for {file_id} in {chat_id}")
            return web.Response(status=410, text="410: Gone. Access to the target resource is no longer available!")

        if thumb and message.document:
            thumbnail = message.document.thumbs
            if not thumbnail:
                log.debug(f"no thumbnail for {file_id} in {chat_id}")
                return web.Response(status=404, text="404: Not Found")
            thumbnail = thumbnail[-1]
            mime_type = 'image/jpeg'
            size = thumbnail.size if hasattr(
                thumbnail, 'size') else len(thumbnail.bytes)
            file_name = f"{file_id}_thumbnail.jpg"
            media = types.InputDocumentFileLocation(
                id=message.document.id,
                access_hash=message.document.access_hash,
                file_reference=message.document.file_reference,
                thumb_size=thumbnail.type
            )
        else:
            media = message.media
            size = message.file.size
            file_name = get_file_name(message)
            mime_type = message.file.mime_type

        try:
            offset = req.http_range.start or 0
            limit = req.http_range.stop or size
            if (limit > size) or (offset < 0) or (limit < offset):
                raise ValueError("range not in acceptable format")
        except ValueError:
            return web.Response(
                status=416,
                text="416: Range Not Satisfiable",
                headers={
                    "Content-Range": f"bytes */{size}"
                }
            )

        if not head:
            body = self.client.download(media, size, offset, limit)
            log.info(
                f"Serving file in {message.id} (chat {chat_id}) ; Range: {offset} - {limit}")
        else:
            body = None

        headers = {
            "Content-Type": mime_type,
            "Content-Range": f"bytes {offset}-{limit}/{size}",
            "Content-Length": str(limit - offset),
            "Accept-Ranges": "bytes",
            "Content-Disposition": f'attachment; filename="{file_name}"'
        }

        return web.Response(
            status=206 if offset else 200,
            body=body,
            headers=headers
        )

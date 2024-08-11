from aiohttp import ClientSession
import time

from anypid.lib.error import HttpError


class ChineseDoiSdk:

    def __init__(self, username: str,
                 password: str,
                 base_url: str = 'http://www.chinadoi.cn/chinadoi-manage/manage') -> None:

        self.username = username
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.session = ClientSession()
        self._last_login_ts = 0

    async def login(self):
        url = f'{self.base_url}/login.action'
        body = {
            'userName': self.username,
            'password': self.password,
            'x': 74, 'y': 20,  # just magic number
        }
        async with self.session.post(url, data=body) as resp:
            text = await resp.text()
            if '欢迎使用中文DOI' not in text:
                raise HttpError(401, 'Login failed!')
        self._last_login_ts = time.time()

    async def close(self):
        await self.session.close()

    async def get_doi(self, doi: str):
        await self._may_refresh_login()
        url = f'{self.base_url}/doiBatchParse.action'
        body = {'doiStr': doi}
        async with self.session.post(url, data=body) as resp:
            text = await resp.text()
            if '命中数：1' not in text:
                raise HttpError(404, 'DOI not found!')
            # TODO: parse html document and return a dict of metadata
            return text

    async def register_doi(self, doi: str, title: str, author: str, journal: str, year: str):
        await self._may_refresh_login()
        ...

    async def _may_refresh_login(self):
        if time.time() - self._last_login_ts > 60:
            await self.login()




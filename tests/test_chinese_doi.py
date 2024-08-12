import unittest
import os

from anypid.provider.chinese_doi import ChineseDoiSdk


class TestChineseDoi(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        username = os.environ.get('CHINESE_DOI_USERNAME')
        passowrd = os.environ.get('CHINESE_DOI_PASSWORD')
        assert username and passowrd, 'Please set CHINESE_DOI_USERNAME and CHINESE_DOI_PASSWORD'
        self.sdk = ChineseDoiSdk(username, passowrd)
        await self.sdk.login()

    async def asyncTearDown(self):
        await self.sdk.close()

    async def test_get_doi(self):
        valid_doi = '10.6043/j.issn.0438-0479.202312005'
        text = await self.sdk.get_doi(valid_doi)
        print(text)


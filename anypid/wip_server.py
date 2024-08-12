from typing import Annotated
from fastapi import FastAPI, Depends

try:
    import toml
except ModuleNotFoundError:
    import pip._vendor.tomli as toml

from anypid.provider.chinese_doi import ChineseDoiSdk

with open("config.toml", "rb") as fp:
    config = toml.load(fp)


_doi_sdk = None
async def get_doi_sdk():
    global _doi_sdk
    if _doi_sdk is None:
        _doi_sdk = ChineseDoiSdk(config['username'], config['password'])
    return _doi_sdk

app = FastAPI()

@app.get("/")
async def get_provider():
    return {}

@app.get("/doi/{doi}")
async def get_metadata(doi: str, doi_sdk: Annotated[ChineseDoiSdk, Depends(get_doi_sdk)]):
    await doi_sdk.get_doi(doi)
    return {"doi": doi}

@app.post("/doi")
async def register_doi(req: dict, doi_sdk: Annotated[ChineseDoiSdk, Depends(get_doi_sdk)]):
    print(req)
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=config.get('port', 8520))


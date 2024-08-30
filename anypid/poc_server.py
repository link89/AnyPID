from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from anypid.lib.error import HttpError
import json
import os

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

@app.get("/doi/{doi:path}")
async def get_metadata(doi: str, doi_sdk: Annotated[ChineseDoiSdk, Depends(get_doi_sdk)]):
    try:
        await doi_sdk.get_doi(doi)
    except HttpError as e:
        raise HTTPException(e.code, e.message)
    return {"doi": doi}

@app.put("/doi/{doi:path}")
async def register_doi(doi: str, req: dict, doi_sdk: Annotated[ChineseDoiSdk, Depends(get_doi_sdk)]):
    data_dir = config.get('data_dir', './data')
    request_file = f'{data_dir}/{doi}.json'
    os.makedirs(os.path.dirname(request_file), exist_ok=True)
    with open(request_file, 'w') as fp:
        json.dump(req, fp, indent=2)
    return {"status": "ok"}


if __name__ == "__main__":
    port=config.get('port', 8520)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)


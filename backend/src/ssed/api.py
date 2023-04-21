from fastapi import FastAPI

from typing import Any


app = FastAPI()


@app.get('/')
async def root() -> dict[str, Any]:
    return {
        'message': 'success'
    }

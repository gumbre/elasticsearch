from elasticsearch import Elasticsearch
from fastapi import FastAPI, Request, Query, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

INDEX_NAME = 'index_name'
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def get_query(query):
    base_query = {
        "min_score": 0.5,
        "query": {
            "multi_match": {
                "query": query,
                "type": "most_fields",
                "fields": [
                    "full_name",
                    "npi",
                    "city",
                    "state"
                ],
                "fuzziness": "AUTO",
                "prefix_length": 3
            }
        }
    }
    return base_query


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/api/search")
async def search(data: str = Form(...)):
    res = es.search(index=INDEX_NAME, body=get_query(data))
    res = res["hits"]["hits"]
    return {"data": res}

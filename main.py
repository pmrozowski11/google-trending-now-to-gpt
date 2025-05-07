from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import re

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/trendy")
def get_trends():
    try:
        url = "https://trends.google.com/_/TrendsUi/data/batchexecute?rpcids=g4kJzf&source-path=%2Ftrending&hl=pl&bl=boq_trends-boq-servers-frontend_20250506.03_p0"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "f.req": '[[["g4kJzf","[[null,null,[6],[],[]]]",null,"generic"]]]'
        }

        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}

        # usuń prefix ")]}'\n" i wyciągnij właściwy JSON
        body = response.text
        cleaned = re.sub(r"^\)\]\}'\n\d+\n", "", body)
        json_blob = json.loads(cleaned)
        inner_json_str = json_blob[0][2]
        inner_json = json.loads(inner_json_str)

        # Parsowanie głównych tematów
        topic_data = inner_json[0]
        topic_names = []

        for entry in topic_data:
            if entry and isinstance(entry, list) and len(entry) > 0:
                title = entry[0]
                if isinstance(title, str):
                    topic_names.append(title)

        return {"trendy": topic_names[:10]}  # top 10 trendów

    except Exception as e:
        return {"error": str(e)}

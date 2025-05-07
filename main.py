from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pytrends.request import TrendReq

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/trendy")
def get_trends():
    try:
        pytrends = TrendReq(hl='pl-PL', tz=360)
        kw_list = ["film", "serial", "muzyka"]  # frazy startowe, by zbudować kontekst
        pytrends.build_payload(kw_list, cat=6, geo='PL', timeframe='now 1-d')
        related = pytrends.related_queries()
        trendy = []
        for keyword, queries in related.items():
            if queries and 'top' in queries and queries['top'] is not None:
                trendy.extend(queries['top']['query'].tolist())
        unique_trendy = list(set(trendy))
        return {"trendy": unique_trendy[:10]}  # zwracamy tylko top 10
    except Exception as e:
        return {"error": str(e)}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pytrends.request import TrendReq

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/trendy")
def get_trends():
    try:
        pytrends = TrendReq(hl='pl-PL', tz=360)
        # trending_searches to lista ogólnych trendów, nie tylko z kategorii "Rozrywka"
        trending_searches_df = pytrends.trending_searches(pn='poland')
        trending = trending_searches_df[0].tolist()
        return {"trendy": trending}
    except Exception as e:
        return {"error": str(e)}

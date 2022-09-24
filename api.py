import json
from fastapi import FastAPI


app = FastAPI()


data = json.load(open('smartphones.json', encoding='utf-8'))



@app.get("/smartphones")
def smartphones(price: int):
    price_matches = [p for p in data if int(p["price"])==price]
    if len(price_matches) != 0:
        return price_matches

    return {"Data": "No items match the specified price"}

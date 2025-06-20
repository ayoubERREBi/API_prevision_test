from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from predict_one_product_sale import forcasting
from typing import List
from datetime import date


class CalCOutput(BaseModel):
    date: date
    item_code: str
    delivered_qty: float
    delivered_qty_non_outliers: float


app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")

def Hi():
    return {"message":"hello test"}



@app.get("/userinfo", response_model=List[CalCOutput])
def get_info(id: str = Query(...)):
    print(f"[INFO] Appel reçu avec id = {id}")
    try:
        f = forcasting()
        prod_75135_2 =  f.choose_prod(id) 
        prod_75135_2 = f.correct_outliers(prod_75135_2)
        print(f"[INFO] Données récupérées : {prod_75135_2}")
        prod_75135_2 = prod_75135_2.rename(columns={
            "Date": "date",
            "Item Code": "item_code",
            "Delivered Qty": "delivered_qty",
            "Delivered Qty_NonOutliers": "delivered_qty_non_outliers"
        })
        prod_75135_2["item_code"] = prod_75135_2["item_code"].fillna(id)
        return prod_75135_2.to_dict(orient="records")
    except Exception as e:
        print(f"[ERREUR] {e}")
        raise HTTPException(status_code=500, detail=str(e))
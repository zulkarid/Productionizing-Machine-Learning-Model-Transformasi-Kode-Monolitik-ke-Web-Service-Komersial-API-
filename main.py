from fastapi import FastAPI
from pydantic import BaseModel
from predictor import OlympicPredictor

app = FastAPI( #untuk inisiasi FastAPI
    title="Olympic Medals Prediction API",
    description="API Komersial untuk memprediksi jumlah perolehan medali Olimpiade suatu negara."
)

predictor = OlympicPredictor()   #memasukkan class predictor yang terhubung dengan model.pkl

class OlympicInput(BaseModel):      #struktur data input menggunakan pydantic (validasi tipe data)
    athletes: float | str  # mengizinkan str agar bisa menggunakan try-except di predictor.py
    prev_medals: float | str

@app.post("/predict")
def predict_endpoint(data: OlympicInput):
    #ubah data berformat json menjadi dictionary python biasa
    input_dict = data.dict()
    
    hasil = predictor.preprocess_and_predict(input_dict) #kirim data ke predictor.py untuk eksekusi
    
    return hasil
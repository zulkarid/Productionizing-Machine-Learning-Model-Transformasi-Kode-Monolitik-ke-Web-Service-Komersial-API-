import pickle
import numpy as np

class OlympicPredictor:
    def __init__(self, model_path='model.pkl'):
        # Memuat model biner secara terisolasi
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def preprocess_and_predict(self, input_data):
        try:
            #ambil data
            jumlah_atlet = input_data['athletes']
            medali_sebelumnya = input_data['prev_medals']
            
            #menkonversikan ke float agar berbentuk numerik
            data_terformat = np.array([[float(jumlah_atlet), float(medali_sebelumnya)]])
            
            #model Linear Regression
            prediksi_mentah = self.model.predict(data_terformat)
            
            hasil_akhir = prediksi_mentah[0] #buat cegah tidak boleh minus
            if hasil_akhir < 0:
                hasil_akhir = 0
            
            # Mengembalikan pembulatan medali ke nilai terdekat 
            return {
                "status": "success",
                "predicted_medals": int(round(hasil_akhir))
            }
            
        except KeyError as e:
            #antisipasi kalau ada parameter yang kurang
            return {
                "status": "error",
                "message": f"Data tidak lengkap! Parameter berikut wajib diisi: {str(e)}"
            }
        except ValueError:
            #antisipasi error kalau user ngirim teks ke kolom numerik
            return {
                "status": "error",
                "message": "Tipe data salah! Input 'athletes' dan 'prev_medals' harus berupa angka."
            }
        except Exception as e: #antisipasi kalau ada error mendadak agar server tidak mati
            return {
                "status": "error",
                "message": f"Terjadi kesalahan pada sistem: {str(e)}"
            }
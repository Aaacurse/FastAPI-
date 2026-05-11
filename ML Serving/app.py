from fastapi import FastAPI
from fastapi.responses import JSONResponse

app=FastAPI()

from schema.cities import tier_1_cities,tier_2_cities
from schema.user_input import UserInput
from model.predict import model,predict_output
     
@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}   

@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'model_loaded': model is not None
    }
        
@app.post('/predict')
def predict_premium(data:UserInput):
    
    user_input=[{
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
    }]
    
    prediction=predict_output(user_input)
    
    return JSONResponse(status_code=200,content={'predicted_category':prediction})
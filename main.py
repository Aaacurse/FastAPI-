from fastapi import FastAPI,Path,HTTPException
import json


app=FastAPI()

def load_data():
    with open('Patient.json','r') as f:
        file=json.load(f)
        
    return file



@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management API"}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description="ID of the patient in DB",examples="P001")):
    #load all patients
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404,detail="Patient not found")
    
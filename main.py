from fastapi import FastAPI
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
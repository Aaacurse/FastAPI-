from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
import json
from typing import Annotated,List,Literal

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='Id of the patient',examples=['P001'])]
    name:Annotated[str,Field(...)]
    city:Annotated[str,Field(...)]
    age:Annotated[int,Field(...,gt=0,le=120)]
    gender:Annotated[Literal["Male","Female","Others"],Field(...)]
    height:Annotated[float,Field(...)]
    weight:Annotated[float,Field(...)]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2))
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "Underweight"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Overweight"
        else:
            return "Obese"
    

app=FastAPI()

def load_data():
    with open('Patient.json','r') as f:
        file=json.load(f)
        
    return file


def save_data(data):
    with open('Patient.json','w') as f:
        json.dump(data,f)


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
    
@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description="Sort on basis of height,weight or bmi"),order:str=Query(default='asc',description="Sort in ascending or descending order")):
    valid_fields=['height','weight','bmi']
    if sort_by.lower() not in valid_fields:
        raise HTTPException(status_code=400,detail=f"""Invalid field select from {valid_fields}""")
    
    if order.lower() not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f"""Invalid field select from asc or desc""")
    data=load_data()
    
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):
    #load existing data
    data=load_data()
    #check if patient exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exits")
    #new patient add to db
    data[patient.id]=patient.model_dump(exclude=['id'])
    #save data
    save_data(data=data)
    
    return JSONResponse(status_code=201,content={"message":"patient created successfully"})
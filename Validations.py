from datetime import date
import re
from fastapi import HTTPException
import Structure


def validate_employee_data(employee_data: Structure.EmployeeBase):
    if not (employee_data.First_Name.isalpha() and employee_data.First_Name.istitle()):
        raise HTTPException(status_code=400, detail="First name must contain only alphabets and start with a capital letter")
    if not (employee_data.Last_Name.isalpha() and employee_data.Last_Name.istitle()):
        raise HTTPException(status_code=400, detail="Last name must contain only alphabets and start with a capital letter")
    
    email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    if not email_pattern.match(employee_data.Email) or '..' in employee_data.Email or '@@' in employee_data.Email :
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    if not employee_data.Phone_Number.isdigit() or len(employee_data.Phone_Number) != 10:
        raise HTTPException(status_code=400, detail="Phone number must be exactly 10 digits") 
    
    today = date.today()
    age = today.year - employee_data.Date_of_Birth.year - ((today.month, today.day) < (employee_data.Date_of_Birth.month, employee_data.Date_of_Birth.day))
    if age < 20:
        raise HTTPException(status_code=400, detail="Employee must be at least 20 years old") 
    
    if employee_data.Date_of_Birth == employee_data.Date_of_Joined:
        raise HTTPException(status_code=400, detail="Date of Birth and Date of Joined should not be the same") 
    
    if not (employee_data.Number_of_Leaves>=10 and employee_data.Number_of_Leaves <= 40):
        raise HTTPException(status_code=400, detail="Number of leaves must be between 10 and 40")
    
    if employee_data.Date_of_Joined and employee_data.Date_of_Joined > date.today():
        raise HTTPException(status_code=400, detail="Date of joining cannot be in the future")
    
    if not isinstance(employee_data.Is_active, bool):
        raise HTTPException(status_code=400, detail="Is_active must be a boolean (True or False)")
    
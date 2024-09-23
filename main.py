from typing import List
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import Structure, Logics, database


app = FastAPI(title="Employee Information")



def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close() 


#------------------------------DepartMentInfo Endpoints -------------------#
@app.post("/departments/", response_model=Structure.Department, tags=["Department"])
def create_department(department: Structure.DepartmentCreate, db: Session = Depends(get_db)):
    return Logics.create_department(db=db, department=department)

@app.get("/departments/{department_id}", tags=["Department"])
def read_department(department_id: int, db: Session = Depends(get_db)):
    db_department = Logics.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department 

@app.get("/departments/", tags=["Department"])
def read_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    departments = Logics.get_departments(db, skip=skip, limit=limit)
    return departments 


@app.put("/departments/{department_id}", response_model=Structure.DepartmentBase, tags=["Department"])
def update_department_endpoint(department_id: int, department_update: Structure.DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = Logics.update_department(db=db, department_id=department_id, department_update=department_update)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department


@app.delete("/departments/{department_id}", tags=["Department"])
def delete_department_endpoint(department_id: int, db: Session = Depends(get_db)):
    db_department = Logics.delete_department(db=db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"Department": "Deleted Successfully"}



#..............EndPoints Of Role_Management.................................................

@app.post("/role/",  tags=["Role"])
def create_role(role:Structure.RoleCreate, db: Session= Depends(get_db)):
    return Logics.create_role(db=db, role=role) 

@app.get("/roles/{role_id}", response_model=Structure.RoleBase, tags=["Role"])
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = Logics.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role 

@app.put("/roles/{role_id}", response_model=Structure.Response_Role, tags=["Role"])
def update_role_endpoint(role_id: int, role_update: Structure.RoleUpdate, db: Session = Depends(get_db)):
    db_role = Logics.update_role(db=db, role_id=role_id, role_update=role_update)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role 

@app.delete("/roles/{role_id}", tags=["Role"])
def delete_role_endpoint(role_id: int, db: Session = Depends(get_db)):
    db_role = Logics.delete_role(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"Role": "Deleted Succesfully"}




#------------------------- EmployeeInfo EndPoints -------------------#

@app.post("/employees/", tags=["Employee_Information"])
def create_employee(employee: Structure.EmployeeCreate, db: Session = Depends(get_db)):
    db_em =  Logics.create_employee(db=db, employee=employee)
    return db_em



@app.get("/employees/{employee_id}", response_model=Structure.Employee, tags=["Employee_Information"])
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = Logics.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.get("/employees/", response_model=list[Structure.Employee], tags=["Employee_Information"])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = Logics.get_employees(db, skip=skip, limit=limit)
    if employees is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees 


@app.put("/employees/{employee_id}", response_model=Structure.Employee, tags=["Employee_Information"])
def update_employee(employee_id: int, employee: Structure.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = Logics.update_employee(db=db, employee_id=employee_id, employee_update=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee 


@app.delete("/employees/{employee_id}", tags=["Employee_Information"])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = Logics.delete_employee(db=db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"Employee_Info": "Deleted Successfully"}




##### .........ENDPOINTS FOR ATTENDENCE................############

@app.post("/attendance/", tags=["Attendance"])
def create_attendance_endpoint(User_id : int, attendance: Structure.AttendanceCreate, db: Session = Depends(get_db)):
    return Logics.create_attendance(db, User_id , attendance)

@app.get("/attendance/{employee_id}", tags=["Attendance"])
def get_attendance_details_endpoint(employee_id: int, db: Session = Depends(get_db)):
    return Logics.get_attendance_details(db, employee_id)


@app.put("/attendance/{User_id}/update", tags=["Attendance"])
def update_attendance_endpoint( User_id: int, attendance_update: Structure.Attendence_Update, db: Session = Depends(get_db)):
    return Logics.update_attendance(db, User_id, attendance_update)




#...........................Endpoints of Leave_Management.......................................................

@app.post("/leave_requests/", tags=["Leave"])
def create_leave_request(User_id : int, leave_request: Structure.LeaveRequestCreate, db: Session = Depends(get_db)):
    return Logics.create_leave_request(db, User_id , leave_request)

@app.get("/leave_requests/employee/{employee_id}", response_model=List[Structure.LeaveRequestResponse], tags=["Leave"])
def read_leave_requests_by_employee(employee_id: int, db: Session = Depends(get_db)):
    leave_requests = Logics.get_leave_requests_by_employee(db, employee_id)
    return leave_requests

@app.get("/leave_requests_pending/manager/{User_id}", tags=["Leave"])
def read_pending_leave_requests_for_manager(User_id: int, db: Session = Depends(get_db)):
    leave_requests = Logics.get_pending_leave_requests_for_manager(db, User_id)

    formatted_requests = [{
        "leave_request": {
            "id": leave.id,
            "start_date": leave.start_date,
            "end_date": leave.end_date,
            "reason": leave.reason,
            "status": leave.status,
            "number_of_days": leave.number_of_days
        },
        "employee_name": f"{first_name} {last_name}"
    } for leave, first_name, last_name in leave_requests ]
    
    return formatted_requests


@app.put("/leave_requests/{leave_request_id}/approve", tags=["Leave"])
def approve_leave_request(leave_request_id: int, approval: Structure.LeaveApproval, db: Session = Depends(get_db)):
    Approval = Logics.approve_leave_request(db, leave_request_id,approval) 

    if Approval.status not in ["Approved", "Rejected"] :
        return {"Mistake": "Check Spelling"} 
    return Approval

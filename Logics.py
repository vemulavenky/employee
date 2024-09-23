from datetime import date
import re
from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

import Tables, Structure
import Validations


def create_employee(db: Session, employee: Structure.EmployeeCreate):
    Validations.validate_employee_data(employee) 
    existing_employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.Email == employee.Email).first()
    if existing_employee:
        raise HTTPException(status_code=400, detail="Employee Alre ady Exists")

    db_employee = Tables.Employee_Information(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee 

def get_employee(db: Session, employee_id: int):
    return db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).filter(Tables.Employee_Information.Is_active == True).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    result = (
        db.query(Tables.Employee_Information)
        .filter(Tables.Employee_Information.Is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return result

def update_employee(db: Session, employee_id: int, employee_update: Structure.EmployeeUpdate):
    Validations.validate_employee_data(employee_update)
    if employee_update.Date_of_Joined and employee_update.Date_of_Joined > date.today():
        raise HTTPException(status_code=400, detail="Date of joining cannot be in the future")
    
    db_employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()
    if db_employee.Department_id:
        if db.query(Tables.Department).filter(Tables.Department.id == employee_update.Department_id).first() is None:
            raise HTTPException(status_code=400, detail="Department_id does not exist")
    if db_employee.Role_id:
        if db.query(Tables.Role).filter(Tables.Role.id == employee_update.Role_id).first() is None:
            raise HTTPException(status_code=400, detail="Role_id does not exist")

    if db_employee:

        db_employee.First_Name = employee_update.First_Name
        db_employee.Last_Name = employee_update.Last_Name
        db_employee.Email = employee_update.Email
        db_employee.Phone_Number = employee_update.Phone_Number
        db_employee.Date_of_Birth = employee_update.Date_of_Birth
        db_employee.Department_id = employee_update.Department_id
        db_employee.Role_id = employee_update.Role_id
        db_employee.Date_of_Joined = employee_update.Date_of_Joined
        db_employee.Is_active = employee_update.Is_active
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()
    if employee:
        if employee.Is_active:
            employee.Is_active = False 
            db.commit()
            return employee
    return None



def get_department(db: Session, department_id: int):
    return db.query(Tables.Department).filter(Tables.Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tables.Department).offset(skip).limit(limit).all() 



def create_department(db: Session, department: Structure.DepartmentCreate):
    
    db_department = Tables.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department 

def update_department(db: Session, department_id: int, department_update: Structure.DepartmentUpdate):
    db_department = db.query(Tables.Department).filter(Tables.Department.id == department_id).first()
    if db_department:
        db_department.Name_of_Department = department_update.Name_of_Department
        db_department.description = department_update.description
        db.commit()
        db.refresh(db_department)
    return db_department




def delete_department(db: Session, department_id: int):
    db_department = db.query(Tables.Department).filter(Tables.Department.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(db_department)
    db.commit()

   

def create_role(db: Session, role: Structure.Role):
    db_role = Tables.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role 

def get_role(db: Session, role_id: int):
    return db.query(Tables.Role).filter(Tables.Role.id == role_id).first()

def update_role(db: Session, role_id: int, role_update: Structure.RoleUpdate):
    db_role = db.query(Tables.Role).filter(Tables.Role.id == role_id).first()
    if db_role:
        db_role.Name_Of_Role = role_update.Name_Of_Role
        db_role.department_id = role_update.department_id
        db.commit()
        db.refresh(db_role)
    return db_role

# Delete a Role
def delete_role(db: Session, role_id: int):
    db_role = db.query(Tables.Role).filter(Tables.Role.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role


def create_attendance(db: Session, User_id : int, attendance: Structure.AttendanceCreate): 

    Manager_employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == User_id ).first()
    if not Manager_employee_details:
        raise HTTPException(status_code=404, detail=f"Manager is Not found") 
    
    if not Manager_employee_details.Is_active:
        raise HTTPException(status_code=403, detail="Inactive Manager or TeamLead cannot mark attendance.")

    
    role = db.query(Tables.Role).filter(Tables.Role.id == Manager_employee_details.Role_id ).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.Name_Of_Role  not in ["Manager", "IT Manager", "Team Lead"] :
        raise HTTPException(status_code=403, detail="Only Managers or Team Leads can mark attendance")
    
    if User_id == attendance.employee_id:
        raise HTTPException(status_code=403, detail="Managers or Team Lead cannot mark attendance for themselves Only Your Put Attendnece for Employees")
    
    employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == attendance.employee_id).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_attendance = Tables.Attendance(
        employee_id=attendance.employee_id,
        date=attendance.date,
        status=attendance.status
    )
    
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

def get_attendance_details(db: Session, employee_id: int):
    employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == employee_id).first()
    if not employee_details:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance_details = db.query(Tables.Attendance).filter(Tables.Attendance.employee_id == employee_id).first()
    role = db.query(Tables.Role).filter(Tables.Role.id == employee_details.Role_id).first()

    if attendance_details:
        employee_presence = "Present"
    else:
        employee_presence = "Absent"

    return {
        "id": employee_details.id,
        "First_Name": employee_details.First_Name,
        "Last_name": employee_details.Last_Name,
        "Role": role.Name_Of_Role,
        "attendance_status": employee_presence
    }

def update_attendance(db: Session, User_id: int, attendance_update: Structure.Attendence_Update):

    Manager_employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id ==User_id).first()
    if not Manager_employee_details:
        raise HTTPException(status_code=404, detail=f"Manager is Not found")
    
    if not Manager_employee_details.Is_active:
        raise HTTPException(status_code=403, detail="Inactive manager cannot mark attendance.")
    
    role = db.query(Tables.Role).filter(Tables.Role.id == Manager_employee_details.Role_id ).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found") 

    if role.Name_Of_Role  not in ["Manager", "IT Manager", "Team Lead"] :
        raise HTTPException(status_code=403, detail="Only Managers or Team Leads can mark attendance")
    
    if User_id == attendance_update.employee_id:
        raise HTTPException(status_code=403, detail="Managers or Team Lead cannot mark attendance for themselves Only Your Put Attendnece for Employees")
    
    employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == attendance_update.employee_id).first()
    if not employee_details:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance = db.query(Tables.Attendance).filter(Tables.Attendance.employee_id == attendance_update.employee_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail=f"No attendance record found for employee")

    attendance.status = attendance_update.status

    db.commit()
    db.refresh(attendance)

    return attendance

def create_leave_request(db: Session,User_id : int, leave_request: Structure.LeaveRequestCreate): 
    Manager_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == User_id).first()
    Role = db.query(Tables.Role).filter(Tables.Role.id == Manager_details.Role_id).first()

    if Role.Name_Of_Role  not in ["Manager", "IT Manager"] :
        raise HTTPException(status_code=403, detail="Sorry Your Not a Manager")
    
    if Manager_details == leave_request.employee_id:
        raise HTTPException(status_code=403, detail="Sorry Your Not a Normal Employee.Leave Request for only Normal Employees")
    
    Employee_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == leave_request.employee_id).first()
    if Employee_details is None :
        raise HTTPException(status_code=404, detail="Employee not found")
        
    number_of_days = (leave_request.end_date - leave_request.start_date).days + 1
    db_leave_request = Tables.Leave(
        employee_id=leave_request.employee_id,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status="Pending",
        number_of_days=number_of_days, 
        approver_id =Manager_details.id
    )
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)

    return db_leave_request

def get_leave_requests_by_employee(db: Session, employee_id: int):
    leave_requests = db.query(Tables.Leave).filter(Tables.Leave.employee_id == employee_id).all()
    return leave_requests


def get_pending_leave_requests_for_manager(db: Session, User_id: int):
    Manager_details = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == User_id).first() 
    Role = db.query(Tables.Role).filter(Tables.Role.id == Manager_details.Role_id).first()

    if Role.Name_Of_Role  not in ["Manager", "IT Manager"] :
        raise HTTPException(status_code=403, detail="Sorry Your Not a Manager")
    
    leave_requests = db.query(Tables.Leave, Tables.Employee_Information.First_Name, Tables.Employee_Information.Last_Name)\
                        .join(Tables.Employee_Information, Tables.Leave.employee_id == Tables.Employee_Information.id)\
                        .filter(Tables.Leave.status == 'Pending', Tables.Leave.approver_id == Manager_details.id)\
                        .all() 
    return leave_requests


def approve_leave_request(db: Session, leave_request_id: int, approval: Structure.LeaveApproval):
    leave_request = db.query(Tables.Leave).filter(Tables.Leave.id == leave_request_id).first()

    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    approver = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == leave_request.approver_id).first()
    if not approver:
        raise HTTPException(status_code=404, detail=f"Approver with ID {leave_request.approver_id} not found")
    
    role = db.query(Tables.Role).filter(Tables.Role.id == approver.Role_id).first()

    if role.Name_Of_Role not in ["Manager", "IT Manager"]:
        raise HTTPException(status_code=403, detail="Only Managers can approve leave requests")
   
    if approval.status == "Approved":
        leave_duration = (leave_request.end_date - leave_request.start_date).days + 1
        employee = db.query(Tables.Employee_Information).filter(Tables.Employee_Information.id == leave_request.employee_id).first()
        if employee.Number_of_Leaves < leave_duration:
            raise HTTPException(status_code=400, detail="Insufficient number of leaves available")
        employee.Number_of_Leaves -= leave_duration

        leave_request.status = "Approved"

    elif approval.status == "Rejected":
        leave_request.status = "Rejected" 

    db.commit()
    db.refresh(leave_request)
    return leave_request
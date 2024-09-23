from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from database import Base, engine

class Employee_Information(Base):
    __tablename__ = 'EmployeeDeatils' 


    id = Column(Integer, primary_key=True) 
    First_Name = Column(String)
    Last_Name = Column(String) 
    Email = Column(String, unique=True,)
    Phone_Number = Column(String, unique=True) 
    Date_of_Birth = Column(Date) 
    Department_id = Column(Integer, ForeignKey('departments.id')) 
    Role_id = Column(Integer, ForeignKey("roles.id")) 
    Number_of_Leaves = Column(Integer, default=30)
    Date_of_Joined = Column(Date) 
    Is_active = Column(Boolean) 

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    Name_of_Department = Column(String, unique=True)
    description = Column(String)  

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True) 
    Name_Of_Role = Column(String, unique=True, index=True)
    department_id = Column(Integer, ForeignKey('departments.id'))


class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('EmployeeDeatils.id'), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
 

class Leave(Base):
    __tablename__ = 'leave'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('EmployeeDeatils.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="Pending")
    number_of_days = Column(Integer)
    approver_id = Column(Integer)

Base.metadata.create_all(bind=engine)
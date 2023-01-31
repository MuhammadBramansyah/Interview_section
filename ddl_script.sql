
-- table employee
create table empl.employees(
    Id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    EmployeeId VARCHAR(10) NOT NULL UNIQUE,
    FullName VARCHAR(100) NOT NULL,
    BirthDate DATE NOT NULL,
    Address VARCHAR(500) 
);


-- table history
create table hstr.history(
    Id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    PosId VARCHAR(10) NOT NULL,
    PosTitle VARCHAR(100) NOT NULL,
    EmployeeId VARCHAR(10) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL
);


-- insert data to table employee
INSERT INTO empl.employees (EmployeeId, FullName, BirthDate, Address) VALUES ('10105001','Ali Anton','19-Aug-82','Jakarta Utara')
INSERT INTO empl.employees (EmployeeId, FullName, BirthDate, Address) VALUES ('10105002','Rara Siva','1-Jan-82','Mandalika')
INSERT INTO empl.employees (EmployeeId, FullName, BirthDate, Address) VALUES ('10105003','Rini Aini','20-Feb-82','Sumbawa Besar')
INSERT INTO empl.employees (EmployeeId, FullName, BirthDate, Address) VALUES ('10105004','Budi','22-Feb-82','Mataram Kota')


-- insert data to table history
INSERT INTO hstr.history (PosId, PosTitle, EmployeeID, StartDate,EndDate) VALUES ('50000','IT Manager','10105001','1-Jan-2022','28-Feb-2022')
INSERT INTO hstr.history (PosId, PosTitle, EmployeeID, StartDate,EndDate) VALUES ('50001','IT Sr. Manager','10105001','1-Mar-2022','31-Dec-2022')
INSERT INTO hstr.history (PosId, PosTitle, EmployeeID, StartDate,EndDate) VALUES ('50002','Programmer Analyst','10105002','1-Jan-2022','28-Feb-2022')
INSERT INTO hstr.history (PosId, PosTitle, EmployeeID, StartDate,EndDate) VALUES ('50003','Sr. Programmer Analyst','10105002','1-Mar-2022','31-Dec-2022')
INSERT INTO hstr.history (PosId, PosTitle, EmployeeID, StartDate,EndDate) VALUES ('50004','IT Admin','10105003','1-Jan-2022','28-Feb-2022')
INSERT INTO hstr.history (PosId, PosTitle, EmployeeID, StartDate,EndDate) VALUES ('50005','IT Secretary','10105003','1-Mar-2022','31-Dec-2022')


-- 1. show all data
with emps as (
    select 
a.EmployeeID,
b.PosId,
a.FullName,
b.PosTitle,
a.BirthDate,
a.Address,
b.StartDate,
b.EndDate
from empl.employees as a
join hstr.history as b 
on a.EmployeeID = b.EmployeeID
),
current_position as (
    select EmployeeID,
           max(StartDate) as max_start_date
    from emps 
    group by EmployeeID
)
select 
    a.EmployeeID,
    a.FullName,
    a.BirthDate,
    a.Address,
    a.PosId,
    a.PosTitle,
    a.StartDate,
    a.EndDate
 from emps as a 
join current_position as b 
on a.EmployeeId = b.EmployeeId and a.StartDate = b.max_start_date

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import ManageEmployee


database = ManageEmployee()


app = FastAPI()


@app.on_event("shutdown")
def shutdown_database_connection():
    print("Ending database connections")
    database.close_connection_pool()


@app.get("/getemployee/{payroll_no}")
async def get_employee(payroll_no: int):
    details = database.get_employee(payroll_no)
    return details


@app.post("/addemployee")
async def add_employee(forename: str, surname:str):
    response = database.insert_employee(forename, surname)
    return {"message": f"Created employee id: {response[1]}"}


@app.delete("/deleteemployee/{payroll_no}")
async def delete_employee(payroll_no: int):
    rowcount = database.delete_employee(payroll_no)
    # return commented out to avoid "Too much data for declared Content-Length"
    # error message. Possibly Fast API delete bug.
    # return JSONResponse(status_code=204, content={})


@app.put("/updateemployee/{payroll_no}")
async def update_employee(payroll_no: int, surname: str):
    rowcount = database.update_employee(payroll_no, surname)
    if rowcount > 0:
        return {"message": f"Updated {rowcount} rows"}
    return JSONResponse(status_code=404, content={"message": "Item not found"})

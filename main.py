"""Start with: python run.py
Reading guide: docs/03-trace-a-request.md. All records are fictional.
"""

# 1. Imports and setup: FastAPI connects HTTP requests to Python functions.
from fastapi import FastAPI, HTTPException
from storage import load_records

app = FastAPI(title="Absence System API", description="Requester / Approver / Request")

@app.get("/")
def welcome():
    return {"message": "Absence System API", "documentation": "/docs"}

# 2. Read all: a Python list becomes a JSON array in the HTTP response.
@app.get("/requesters")
def list_requesters():
    return load_records("requesters.json")

# 3. Read one: URL input -> load -> find -> return, or report not found.
@app.get("/requesters/{requester_id}")
def get_requester(requester_id: int):
    # int lets FastAPI check/convert this URL parameter before calling us.
    requesters = load_records("requesters.json")
    for requester in requesters:
        if requester["requester_id"] == requester_id:
            return requester
    # Outside the loop: only report absence after inspecting all records.
    raise HTTPException(status_code=404, detail="Requester not found")

# The same read pattern, applied to the other concepts from our UML model.
@app.get("/approvers")
def list_approvers():
    return load_records("approvers.json")

@app.get("/approvers/{approver_id}")
def get_approver(approver_id: str):
    for approver in load_records("approvers.json"):
        if approver["approver_id"] == approver_id:
            return approver
    raise HTTPException(status_code=404, detail="Approver not found")

@app.get("/requests")
def list_requests():
    return load_records("requests.json")

# 4. Relationships: both IDs identify a response in this small model.
@app.get("/requests/{requester_id}/{approver_id}")
def get_response(requester_id: int, approver_id: str):
    for response in load_records("requests.json"):
        if (response["requester_id"] == requester_id
                and response["approver_id"] == approver_id):
            return response
    raise HTTPException(status_code=404, detail="Response not found")

# Try /requesters/1002, /requesters/9999 and /requesters/abc in /docs.
# Then trace /requests/1001/IS101 to the two linked records.
# This first API reads data. The optional registration_demo.py writes one record.

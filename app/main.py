from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "QAForge Backend is Running"}

@app.get("/api/test-cases")
def get_test_cases():
    return {
        "test_cases": [
            {
                "id": 1,
                "name": "Login with valid credentials",
                "status": "PASSED"
            },
            {
                "id": 2,
                "name": "Login with invalid password",
                "status": "FAILED"
            }
        ]
    }

@app.post("/api/test-cases")
def create_test_case(test_case: dict):
    return {
        "message": "Test case created successfully"
    }

@app.delete("/api/test-cases")
def delete_test_cases():
    return {
        "message": "All test cases deleted successfully"
    }


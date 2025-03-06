from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import CareerCrew

app = FastAPI() # Initialize FastAPI application

# Define request model for user input

class UserInput(BaseModel):
    skills: str
    interests: str

@app.post("/get_career_suggestions")
async def get_career_suggestions(user_input: UserInput):
    try:
        crew = CareerCrew().career_crew(user_input.skills, user_input.interests) # Create CareerCrew instance and execute career guidance process
        results = crew.kickoff()
        return {"career_suggestions": str(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # Handle errors and return appropriate HTTP response
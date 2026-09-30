import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai

app = FastAPI(title="EduGenie API")

# Templates கோப்பகத்தை அமைத்தல்
templates = Jinja2Templates(directory="templates")

# Gemini Client
client = genai.Client(api_key="AQ.Ab8RN6ELyLzW3a2s82EBVAJLJ_Wcmqp14v61jy2x387WCpRQ")

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "ai_response": None})

@app.post("/ask", response_class=HTMLResponse)
async def ask_edugenie(request: Request, prompt: str = Form(...)):
    """User கேட்கும் கேள்விக்கு Gemini API மூலமாக பதில் வாங்கும் function"""
    try:
        # Gemini Model மூலம் பதிலை உருவாக்குதல்
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        ai_response = response.text
    except Exception as e:
        ai_response = f"Error occurred: {str(e)}"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "prompt": prompt, "ai_response": ai_response}
    )
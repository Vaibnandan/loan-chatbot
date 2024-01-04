from fastapi import Depends, FastAPI, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("messanger.html", {"request": request})

@app.post('/webhook')
async def webhook(request: Request):
    payload = await request.json()
    intent = payload.get("queryResult", {}).get("intent", {}).get("displayName")

    if intent == "signup_intent":
        return RedirectResponse(url="/signup")
    elif intent == "LAP_intent":
        return RedirectResponse(url="/lap")
    elif intent == "business_intent":
        return RedirectResponse(url="/business")
    elif intent == "working_capital_intent":
        return RedirectResponse(url="/workingcapital")
    elif intent == "thank_you":
        return RedirectResponse(url="/thankyou")
    # Add more conditions for other intents if needed"

    # Handle other intents or provide a default response
    response_data = {
        'fulfillmentText': 'Received webhook request'
    }
    return JSONResponse(content=response_data)

@app.get('/signup', response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})
signed_up_users = {}
@app.post('/signup', response_class=HTMLResponse)
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...), mobile: str = Form(...)):
   
    # Perform signup logic here, for example, store the user in a database.
    # You should replace this with your actual signup logic
    signed_up_users[username] = {'password': password, 'mobile': mobile}


    # For demonstration purposes, let's print the values.
    print('Username:', username)
    print('Password:', password)
    print('Mobile Number:', mobile)

    # For demonstration purposes, let's assume successful signup and redirect to a success page.
    return templates.TemplateResponse("sign_up.html", {"username": username, "request": request})

@app.get('/thankyou', response_class=HTMLResponse)
async def thankyou(request: Request):
    return templates.TemplateResponse("thankyou.html", {"request": request})

@app.get('/lap', response_class=HTMLResponse)
async def lap(request: Request):
    return templates.TemplateResponse("LAP.html", {"request": request})

@app.get('/business', response_class=HTMLResponse)
async def business(request: Request):
    return templates.TemplateResponse("business.html", {"request": request})

@app.get('/workingcapital', response_class=HTMLResponse)
async def working_capital(request: Request):
    return templates.TemplateResponse("workingcapital.html", {"request": request})

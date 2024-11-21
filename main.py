from fastapi import FastAPI, Request
from jokes import get_random_joke
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def get_joke():
    return get_random_joke()

@app.get('/pretty/', response_class=HTMLResponse)
def get_pretty_joke(request: Request):
    joke = get_random_joke()
    return templates.TemplateResponse('joke_template.html', {'request': request, 'joke': joke})
from fastapi import FastAPI, Request, Response, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from joke import Joke
from sqlalchemy import func

sqlite_file_name = "jokes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app is start")
    create_db_and_tables()
    yield
    print("APP IS STOPPED")

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory='templates')

@app.post('/')
def post_joke(joke: Joke, session: SessionDep) -> Joke:
    session.add(joke)
    session.commit()
    session.refresh(joke)
    return joke

def get_random_joke(session):
    joke = session.exec(select(Joke).order_by(func.random())).first()
    return joke.content

@app.get('/')
def get_joke(session: SessionDep) -> str | None:
    return get_random_joke(session)
    

@app.get('/pretty/', response_class=HTMLResponse)
def get_pretty_joke(request: Request, session: SessionDep):
    return templates.TemplateResponse('joke_template.html', {'request': request, 'joke': get_random_joke(session)})
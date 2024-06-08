from fastapi import FastAPI, Request

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from openai import OpenAI






app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



def render(path: str, request: Request, context={}):
    return templates.TemplateResponse(
        request=request, name=path, context=context
    )


@app.get("/")
async def root(r: Request):
    return render("inicio.html", r)




@app.get("/preexistente")
async def preexistente(r: Request, mail: str = ""):
    return render("preexistente.html", r, {"mail": mail})


@app.post("/preexistente")
async def preexistente(r: Request, mail: str = ""):
    return render("preexistente.html", r, {"mail": mail})




@app.get("/frases-ideas")
async def preexistente(r: Request):
    return render("frases-ideas.html", r)



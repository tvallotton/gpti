from fastapi import FastAPI, Request, Form, Depends, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import AsyncOpenAI
import json


client = AsyncOpenAI()
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
def get_preexistente(r: Request, mail: str = ""):
    response = mail
    return render("preexistente.html", r, { "mail": mail})


@app.get("/frases-ideas")
def get_frases_ideas(r: Request):
    return render("frases-ideas.html", r)


@app.get("/plantillas")
def plantillas(r: Request): 
    return render("plantillas.html", r)


@app.websocket("/response-stream")
async def websocket_endpoint(websocket: WebSocket):
    segment_template = templates.get_template("segment.html")

    await websocket.accept()

    while True:
        data = json.loads(await websocket.receive_text())
        prompt = templates.get_template("prompt.txt").render(data)
        
        stream = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}],
            stream=True,
        )

        async for chunk in stream:
            print("chunk", chunk)
            segment = chunk.choices[0].delta.content
            print("segment", segment)
            if segment is not None:
                await websocket.send_text(segment_template.render({"segment": segment }))

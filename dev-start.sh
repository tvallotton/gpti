#!/bin/sh

pip install -r requirements.txt
fastapi run --reload --port $PORT


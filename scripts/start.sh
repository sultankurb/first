#!/bin/bash

alembic upgrade head
cd /app
python3 main.py

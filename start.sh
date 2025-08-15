#!/bin/bash
# Railway startup script
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 src.main:app
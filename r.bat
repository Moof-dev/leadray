@echo off
set HOST=127.0.0.1
set PORT=8000

IF "%1"=="fastapi" (
    goto run_fastapi
) ELSE (
    goto help
)

:run_fastapi
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file .env
pause
exit
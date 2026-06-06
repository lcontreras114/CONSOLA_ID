@echo off
echo ===========================================
echo   AUDITSA - Digital Audit - Iniciando...
echo ===========================================

:: Start FastAPI backend in a new window
start "AUDITSA Backend" cmd /k "uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"

:: Wait 2 seconds for backend to start
timeout /t 2 /nobreak >nul

:: Start Streamlit frontend in a new window
start "AUDITSA Frontend" cmd /k "streamlit run frontend/app.py"

echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:8501
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Ambos servicios iniciados. Cierra las ventanas para detenerlos.

@echo off
setlocal

echo Lancement de Port Scanner...
echo Assurez-vous d'avoir Python 3 installe et accessible via la commande "python".
echo.

python main.py

if %errorlevel% neq 0 (
    echo Une erreur est survenue pendant l'execution. Verifiez que Python est installe et que les dependances sont presentes.
)

endlocal

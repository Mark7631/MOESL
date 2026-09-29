@echo off
chcp 65001 > nul

if not exist "venv" (
    echo Создание .venv
    python -m venv .venv
    if errorlevel 1 (
        echo Не удалось создать .venv
        goto end
    )
)

call .venv\Scripts\activate

if exist "requirements.txt" (
    echo Установка зависимостей в .venv.
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo Файл requirements.txt не найден. Приложение не будет запущено.
    goto end
)

echo Запуск приложения.
python ./src/main.py

:end
echo.
echo Конец работы приложения.
pause

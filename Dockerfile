FROM python:3.12-slim

WORKDIR /app

ENV SDL_VIDEODRIVER=dummy \
    SDL_AUDIODRIVER=dummy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cricket_game ./cricket_game
COPY tests ./tests
COPY main.py .

# This container is intended for headless automated tests.
# Run the graphical game locally with: python main.py
CMD ["python", "-m", "pytest", "-v"]

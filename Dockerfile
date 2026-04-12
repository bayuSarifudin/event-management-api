FROM python:3.10-slim

WORKDIR /app

# install system's dependency
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# copy dependency list
COPY requirements.txt .

# install python packages
RUN pip install --no-cache-dir -r requirements.txt

# copy all project's files
COPY . .

# run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
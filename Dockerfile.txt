# 1. Use a lightweight version of Python
FROM python:3.10-slim

# 2. Install system dependencies
# FIX: 'libgl1-mesa-glx' is replaced by 'libgl1' for newer Debian versions
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /app

# 4. Copy your project files
COPY . .

# 5. Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# 6. Start the server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
# Gunakan Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy file requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua kode ke dalam container
COPY . .

# Port yang digunakan (ubah sesuai kebutuhan)
EXPOSE 8000

# Command untuk menjalankan aplikasi (ubah jika pakai Flask)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

ARG PORT=8501
ENV PORT=${PORT}
EXPOSE ${PORT}

# Run Streamlit (allows `$PORT` override at runtime)
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]

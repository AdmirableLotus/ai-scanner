# Red Lotus Scan Backend

A secure Flask backend for analyzing code vulnerabilities using AI and static analysis.

## Security Features

- **Input Validation**: Sanitizes code input to prevent injection attacks
- **CORS Protection**: Restricts origins to localhost:5173 only
- **Rate Limiting**: 10 requests per minute, 50 per hour, 200 per day
- **Error Handling**: Secure error responses without information leakage
- **Logging**: Comprehensive security event logging

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Ollama is running with Unisast model:
```bash
ollama serve
ollama pull unisast
```

3. Run the application:
```bash
python app.py
```

## API Endpoints

### POST /analyze
Analyzes code for vulnerabilities.

**Request:**
```json
{
  "code": "your code here"
}
```

**Response:**
```json
{
  "analysis": "vulnerability analysis results"
}
```

## Rate Limits
- 10 requests per minute per IP
- 50 requests per hour per IP  
- 200 requests per day per IP
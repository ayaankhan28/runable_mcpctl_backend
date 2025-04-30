# MCPCTL Backend

A robust backend implementation for the MCPCTL (Master Control Program Control) system.

## 🚀 Overview

This backend service provides essential functionality for managing and controlling MCP operations through a RESTful API interface.

## 🛠️ Tech Stack

- Python
- FastAPI
- Docker
- PostgreSQL
- Redis

## 🔧 Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ayaankhan28/runable_mcpctl_backend.git
   cd runable_mcpctl_backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## 🔄 API Endpoints

- `/health`: Health check endpoint
- `/api/v1/...`: API endpoints (detailed documentation coming soon)

## 🧪 Testing

```bash
pytest tests/
```

## 📦 Deployment

The application can be deployed using Docker:

```bash
docker-compose up -d
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
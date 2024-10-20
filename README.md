# Rule Engine with AST

A flexible rule engine application that uses Abstract Syntax Trees (AST) to evaluate complex business rules.

## Project Structure
```
rule-engine/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── rule_engine.py
│   │   └── database.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_rule_engine.py
│   │   └── test_api.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── RuleEngine.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB 4.4+
- Docker and Docker Compose (optional)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/kartikgupta14/rule-engine.git
cd rule-engine
```

2. Start the application using Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Manual Setup

### Backend Setup

1. Create and activate a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

### MongoDB Setup

1. Start MongoDB service
2. Create a database named 'rule_engine'
3. Update the MongoDB connection string in `backend/app/database.py` if needed

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Usage Examples

1. Create a new rule:
```bash
curl -X POST http://localhost:8000/rules/create \
  -H "Content-Type: application/json" \
  -d '{"rule": "(age > 30 AND department = \"Sales\")"}'
```

2. Evaluate a rule:
```bash
curl -X POST http://localhost:8000/rules/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "rule_ast": {"type": "operator", "operator": "AND", ...},
    "data": {"age": 35, "department": "Sales"}
  }'
```

## API Documentation

Full API documentation is available at http://localhost:8000/docs when the backend server is running.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

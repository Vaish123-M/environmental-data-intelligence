# Contributing to Environmental Data Intelligence

Thank you for your interest in contributing! This guide will help you set up your development environment and contribute to the project.

## Getting Started

### Prerequisites
- Python 3.10+ and pip
- Node.js 16+ (for frontend work)
- Git

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/environmental-data-intelligence.git
   cd environmental-data-intelligence
   ```

2. **Set up Python environment** (backend):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   source .venv/bin/activate     # macOS/Linux
   
   pip install -r backend/requirements.txt
   pip install -r backend/requirements-dev.txt
   ```

3. **Set up frontend** (optional):
   ```bash
   cd frontend
   npm install
   ```

4. **Verify installation**:
   ```bash
   pytest -q                      # Run tests
   python -m black --check .      # Check formatting
   ```

## Development Workflow

### Running Locally

**Backend**:
```bash
uvicorn backend.app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm start
```

**Model training/tuning**:
```bash
python ml/train_model.py          # Basic training
python ml/tune_and_train.py       # Hyperparameter tuning
python ml/evaluate_model.py       # Evaluation and residuals plot
```

### Code Quality

We enforce code quality standards:

1. **Format code** with Black:
   ```bash
   black backend ml
   ```

2. **Lint** with Ruff:
   ```bash
   ruff check --fix backend ml
   ```

3. **Type check** with Mypy:
   ```bash
   mypy backend
   ```

4. **Run tests**:
   ```bash
   pytest --cov=backend --cov-report=term-missing
   ```

All pull requests must pass these checks (enforced by GitHub Actions CI).

## Making Changes

### Branch Naming
- Feature: `feature/short-description`
- Bugfix: `fix/short-description`
- Docs: `docs/short-description`

### Commit Messages
Use conventional commits:
```
feat: add feature X
fix: resolve issue Y
docs: update README
test: add test coverage for Z
```

### Pull Requests
1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit
3. Push: `git push origin feature/my-feature`
4. Open a PR on GitHub with a description of changes
5. Ensure CI passes (tests, lint, type checks)
6. Request review from maintainers

## Testing

### Writing Tests

Tests live in `backend/tests/`. Example test:

```python
# backend/tests/test_example.py
import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest backend/tests/test_api.py

# Run with verbose output
pytest -v
```

## Project Structure
```
environmental-data-intelligence/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # API endpoints
│   │   ├── model.py           # Model wrapper
│   │   ├── schemas.py         # Request/response schemas
│   │   ├── database.py        # SQLAlchemy models
│   ├── models/                # Saved models & metadata
│   ├── tests/                 # Unit & integration tests
│   ├── requirements.txt        # Production dependencies
│   └── requirements-dev.txt    # Development dependencies
├── ml/                         # ML pipeline
│   ├── train_model.py         # Basic training script
│   ├── tune_and_train.py      # Hyperparameter tuning
│   ├── evaluate_model.py      # Evaluation & metrics
│   ├── preprocess.py          # Shared preprocessing
│   └── sample_data/           # Sample datasets
├── frontend/                   # React frontend
├── .github/workflows/ci.yml    # GitHub Actions CI
├── MODEL_CARD.md              # Model documentation
├── QUICKSTART.md              # Quick setup guide
└── README.md                  # Project overview
```

## Improving the Project

### Areas We'd Love Help With
1. **Feature engineering**: Add more derived features (e.g., rolling averages, lag features)
2. **Model improvements**: Try deep learning (TensorFlow/PyTorch), ensemble methods
3. **Frontend**: Enhance UI with better visualizations, real-time updates
4. **Data**: Integrate more datasets (NASA, NOAA, ESA)
5. **Documentation**: Improve docstrings, add tutorials, create demo notebooks
6. **Testing**: Add more edge-case and integration tests
7. **DevOps**: Improve Docker setup, add Kubernetes manifests

### Contribution Ideas
- **🐛 Bug fixes**: Found a bug? Open an issue or PR.
- **📚 Documentation**: Improve README, add examples, create guides.
- **✨ Features**: Propose new endpoints, model types, or UI components.
- **🧪 Tests**: Increase test coverage and add edge case tests.
- **⚡ Performance**: Profile and optimize slow operations.

## Issues & Questions

- **Questions?** Open a GitHub Discussion or issue.
- **Found a bug?** Please report it with steps to reproduce.
- **Feature request?** Describe the use case and expected behavior.

## Code of Conduct

Be respectful and constructive. This is an educational project open to all levels of contributors.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🚀

# HealthIS-backend
- Serves the healthIS frontend
- Health Information System

## Setup

### Prerequisites
- Python 3.9+
- pip
- Git


### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/healthis.git
cd healthis
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install required packages**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py migrate
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Start the development server**

```bash
python manage.py runserver
```

The app should now be running at:  
`http://127.0.0.1:8000/`

## API Endpoints Overview

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/api/v1/clients/` | GET, POST | List all clients / Register new client |
| `/api/v1/clients/<uuid>/` | GET | View specific client profile |
| `/api/v1/programs/` | GET, POST | List/Create health programs |
| `/api/v1/enrollments/` | POST | Enroll client into a program |


## Run tests

```bash
python manage.py test
```

# Fashion Hub - Clothing E-commerce Website

A modern e-commerce platform for both new and thrift clothing.

## Features
- Separate sections for new and thrift clothing
- User authentication
- Shopping cart functionality
- Product categories
- Responsive design

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the website. 
# Tianjin Fiber Net - Premium Django Portfolio

A premium, agency-quality Django portfolio website utilizing Tailwind CSS (standalone), Swiper.js, Alpine.js, and AOS.js.

## Features
- **Design System**: Fully custom Tailwind CSS configuration using Deep Blue, Magenta, Gold, and Cream.
- **Interactions**: Cinematic hero slider (Swiper.js), scroll animations (AOS.js), and interactive product modals (Alpine.js).
- **Backend**: Fully functional AJAX contact form with Django models. Hardcoded data in `core/data.py` ready to be swapped with DB models later.

## Prerequisites
- Python 3.11+
- Node.js (for Tailwind CLI)

## Setup Instructions

1. **Activate Virtual Environment** (if not already active)
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node Dependencies (Tailwind)**
   ```bash
   npm install
   ```

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Development Workflow

You need two terminal windows running simultaneously for development:

**Terminal 1 (Django Server):**
```bash
python manage.py runserver
```

**Terminal 2 (Tailwind Watch):**
```bash
npm run dev
```

## Production Build

To compile and minify the CSS for production, run:
```bash
npm run build
```

## Future Database Integration

Currently, pages like Home, About, and Services use hardcoded data from `core/data.py`. 
To transition to a database-backed CMS:
1. Create models in `core/models.py` (e.g., `Product`, `Service`, `FAQ`).
2. Run `python manage.py makemigrations` and `python manage.py migrate`.
3. Update `core/views.py` to query these models (e.g., `Product.objects.all()`) instead of importing from `data.py`.
4. Register the models in `core/admin.py` to manage them via the Django Admin interface.

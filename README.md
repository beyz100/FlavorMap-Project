# FlavorMap

FlavorMap is a web application for exploring and discovering restaurants.

## Setup Instructions

Follow these steps to set up the project locally on your machine.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd FlavorMap-Project
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   Open your web browser and go to [http://localhost:8000](http://localhost:8000).

## Project Apps

- `flavormap`: Main project configuration and routing.
- `restaurants`: Core application handling restaurant models, views, and templates.
- `users`: Application dedicated to user authentication and profile management.
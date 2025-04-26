# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# management commands
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
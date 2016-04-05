# postup spouštění a ovládání django

# miniconda (conda) - mám udělaný virtual. env. "molinf" se vším nainstalováno
activate molinf

# v root directory django projectu
python manage.py runserver  # spustí zkušební server
python manage.py makemigrations # připraví databázi
python manage.py migrations     # update databáze
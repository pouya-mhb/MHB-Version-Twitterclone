# MHB Version of Twitter clone
## This is a forked project of twitter clone project of mundo-python's project

1.Clone The project

```git clone https://github.com/pouya-mhb/MHB-Version-Twitterclone.git```


2. Create Virtual environment

```python -m venv socialenv```
or
```virtualenv env```


3. Install packages from requirements.txt

```pip install -r requirements.txt```


4. Create migrations and migrate

```python manage.py makemigrations```
```python manage.py migrate```


5. Create admin user

```python manage.py createsuperuser```

6. Run the project

```python manage.py runserver```

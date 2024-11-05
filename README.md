Python version: `3.12.7`

##### Verificar versão do Django
```python
>>> import django
>>> django.get_version()
'5.1.2'
```

##### Gerar migrations
```bash
python manage.py makemigrations
```

##### Aplicar Migrations
```bash
python manage.py migrate
```

##### Executar servidor
```bash
python manage.py runserver
```

##### Gerar uma SECRET_KEY (`settings.py`), caso necessário
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Python version: `3.12.7`

##### Verificar versão do Django
```python
>>> import django
>>> django.get_version()
'5.1.2'
```

##### Variáveis ambiente
Copiar arquivo `local_settings_example.py` para `local_settings.py` na raiz `myblog`
Em seguida, ajustar conforme ambiente (database, allowed_hosts, debug,...)

##### Gerar migrations
```bash
python manage.py makemigrations
```

##### Aplicar Migrations
```bash
python manage.py migrate
```

##### Criar SuperUser
```bash
python manage.py createsuperuser
```
Preencher os campos `Usuário`, `Endereço de E-mail` e `Password` e `Password(again)`


##### Executar servidor
```bash
python manage.py runserver
# ou executar em um host:porta personalizado
python manage.py runserver 127.0.0.1:8001
```

##### Gerar uma SECRET_KEY (`settings.py`), caso necessário
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# 8ad!*kcmdkS*zs6h4hktlx_td4&zlxst-b450a!09@9ui8x@3
```
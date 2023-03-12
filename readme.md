Selamlar,

Repoyu nest.js ile yazmadım. Django'ya hakimiyetim daha yüksek olduğundan dolayı django ile yazdım.

Database Schema'yı reponun rootunda görselleştirilmiş şekilde bulabilirsiniz
Request modelinden kastınızı anlayamadım web dev'de yeniyim ancak api/views.py dosyası içinde her endpoint için açıklamalar bulunmaktadır.

Zamanı geldiğinde subscription'a ait order'in oluşturulması için celery kullanıldı. Celery ile birlikte redis kullanıldı.


## Kurulum
Dependency'ler
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Redis
```bash
brew install redis
redis-server
```

## Kullanım

### Server
```bash
cd server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Farklı bir terminalde
```bash
Celery
```bash
cd server
celery -A server worker --loglevel=INFO -B
```



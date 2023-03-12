## Giriş
### Selamlar
Repoyu nest.js ile yazmadım. Django'ya hakimiyetim daha yüksek olduğundan dolayı django ile yazdım.
Database Schema'yı reponun rootunda görselleştirilmiş şekilde bulabilirsiniz
Requestleri modellemekten kastınızı anlayamadım web dev'de yeniyim ancak api/views.py dosyası içinde her endpoint için açıklamalar bulunmaktadır.


### Kullanılan Teknolojiler
- Django
- Django Rest Framework
- Celery
- Redis
- SQLite

Zamanı geldiğinde subscription'a ait order'in oluşturulması için celery kullanıldı. Celery ile birlikte redis kullanıldı.

### Naming Convention
- Model isimleri CamelCase
- Model field isimleri snake_case
- Endpointler /model/id/action/id şeklinde oluşturuldu Örnek olarak /subscription/create ya da /subscription/1/order/create


### Endpointler
Projede çalışan bütün endpointler api/views.py dosyasında bulunmaktadır. ve url'leri api/urls.py dosyasında bulunmaktadır. Bu dosyada bulunan örnek /user/create endpointi djangonun yapısından dolayı gerçekte /api/user/create endpointine karşılık gelmektedir.


## Kurulum
### Dependency'ler
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Redis
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

### Celery
Farklı bir terminalde
```bash
```bash
cd server
celery -A server worker --loglevel=INFO -B
```



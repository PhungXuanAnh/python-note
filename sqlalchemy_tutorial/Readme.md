Các bước code được thực hiện theo link: [https://docs.sqlalchemy.org/en/latest/orm/tutorial.html](https://docs.sqlalchemy.org/en/latest/orm/tutorial.html)

# Tạo database server

Có thể test với postgreSQL hoặc Mysql bằng lệnh bên dưới

## PostgreSQL

```shell
docker run -d --name postgres-sqlalchemy-tutorial \
		 -e POSTGRES_PASSWORD=12345 \
		 -e POSTGRES_USER=root \
		 -e POSTGRES_DB=my_test_db \
		 -p 1234:5432 \
		 postgres
```         

## MySQL

```shell
docker run -d --name mysql-sqlalchemy-tutorial \
         -e MYSQL_ROOT_PASSWORD=12345 \
         -e MYSQL_USER=other_user \
         -e MYSQL_PASSWORD=password_for_other_user \
         -e MYSQL_DATABASE=my_test_db \
         -p 4321:3306 \
         mysql:5.7 \
         --character-set-server=utf8 \
         --collation-server=utf8_unicode_ci
```

# Cấu trúc thư mục

[config.py](config.py): chứa các config để kết nối đến db server
[models.py](models.py): chứa các định nghĩa về model
[main.py](main.py): chứa các hàm thao tác với db, gồm tạo data, clean data...


# Cách test
- Chạy hàm [main.py](main.py)
- Chạy create db trước
- Bỏ comment các hàm muốn test rồi chạy
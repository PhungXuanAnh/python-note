Các bước code được thực hiện theo [link](https://docs.sqlalchemy.org/en/latest/orm/tutorial.html)

- [1. Tạo database server](#1-tạo-database-server)
- [2. Cấu trúc thư mục](#2-cấu-trúc-thư-mục)
- [3. Cách test](#3-cách-test)

# 1. Tạo database server

[PostgreSQL](https://github.com/PhungXuanAnh/tech-note/blob/master/devops/docker/docker-command.md#43-postgresql)

[MySQL](https://github.com/PhungXuanAnh/tech-note/blob/master/devops/docker/docker-command.md#44-mysql)

# 2. Cấu trúc thư mục

- [config.py](config.py): chứa các config để kết nối đến db server
- [models.py](models.py): chứa các định nghĩa về model
- [sqlalchemy_sample.py](sqlalchemy_sample.py): chứa các hàm thao tác với db, gồm tạo data, clean data...


# 3. Cách test
- Chạy hàm [sqlalchemy_sample.py](sqlalchemy_sample.py)
- Chạy create db trước
- Bỏ comment các hàm muốn test rồi chạy
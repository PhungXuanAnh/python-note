"""
Reference: https://github.com/PyMySQL/PyMySQL
    1. Install: pip install PyMySQL
    2. Create mysql server:
			sudo rm -rf /tmp/test-mysql-data
			docker rm -f test-mysql
            docker run -d --name test-mysql \
				-p 3306:3306 \
				-v /tmp/test-mysql-data:/var/lib/mysql/ \
				-e MYSQL_ROOT_PASSWORD=passwd \
				-e MYSQL_USER=user \
				-e MYSQL_PASSWORD=passwd \
				-e MYSQL_DATABASE=db \
				mysql:5.7 \
				--character-set-server=utf8 \
         		--collation-server=utf8_unicode_ci

"""
import pymysql
import pymysql.cursors

create_table_sql = """
CREATE TABLE IF NOT EXISTS `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;
"""

connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)


with connection:
    with connection.cursor() as cursor:
        cursor.execute(create_table_sql)

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)

import random
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
redis_cli = redis.Redis(connection_pool=pool)

pipe = redis_cli.pipeline()


def create_data():
    user_id = 100000
    while user_id:
        redis_cli.setbit('article1:today', user_id, random.choice([1, 1, 1, 0]))
        redis_cli.setbit('article2:today', user_id, random.choice([1, 1, 1, 0, 0]))
        redis_cli.setbit('article3:today', user_id, random.choice([1, 1, 1, 0, 0, 0, 0]))
        user_id = user_id - 1


def print_users_read_article():
    print('So luong nguoi dung da xem bai bao 1: ', redis_cli.bitcount('article1:today'))


def print_users_read_a_article():
    pipe.bitcount('article1:today')
    pipe.bitcount('article2:today')
    pipe.bitcount('article3:today')
    print('Tong so nguoi da xem moi bai bao la: ', pipe.execute())


def print_num_article_123user_read():
    pipe.getbit('article1:today', 123)
    pipe.getbit('article2:today', 123)
    pipe.getbit('article3:today', 123)
    print('So bai bao nguoi dung 123 da xem ngay hom nay: ', sum(pipe.execute()))


def print_user123_read_2_article():
    # pipe.setbit('user123', 123, 1)
    # pipe.bitop('AND', '123:sawboth', 'user123', 'article1:today', 'article3:today')
    pipe.bitop('AND', '123:sawboth', 'article1:today', 'article3:today')
    pipe.getbit('123:sawboth', 123)
    # pipe.delete('123:sawboth', 'user123')
    # print('Nguoi dung 123 da xem 2 bai bao ngay hom nay? ', bool(pipe.execute()[2]))
    print('Nguoi dung 123 da xem 2 bai bao ngay hom nay? ', bool(pipe.execute()[1]))


def print_users_read_atleast_one():
    pipe.bitop('OR', 'atleastonearticle', 'article1:today', 'article2:today', 'article3:today')
    pipe.bitcount('atleastonearticle')
    pipe.delete('atleastonearticle')
    print('So nguoi xem it nhat mot bai bao hom nay: ', pipe.execute()[1])


def print_recommendation():
    pipe.bitop('XOR', 'recommendother', 'article1:today', 'article2:today')
    pipe.bitop('AND', 'recommend:article1', 'recommendother', 'article2:today')
    pipe.bitop('AND', 'recommend:article2', 'recommendother', 'article1:today')
    pipe.bitcount('recommendother')
    pipe.bitcount('recommend:article1')
    pipe.bitcount('recommend:article2')
    pipe.delete('recommendother', 'recommend:article1', 'recommend:article2')
    result = pipe.execute()
    print('So nguoi chua doc ca 2 bai bao: ', result[3])
    print('So nguoi da doc bai 2, va se gioi thieu bai 1: ', result[4])
    print('So nguoi da doc bai 1, va se gioi thieu bai 2: ', result[5])


if __name__ == '__main__':
    # create_data()
    # print_users_read_article()
    # print_users_read_a_article()
    # print_num_article_123user_read()
    print_user123_read_2_article()
    # print_users_read_atleast_one()
    # print_recommendation()

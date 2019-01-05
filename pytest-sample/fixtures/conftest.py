import pytest
import smtplib


# @pytest.fixture(scope='module')
# def smtp_connection():
#     smtp_connection = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
#     yield smtp_connection   # provide the fixture value
#     print('teardown smtp')
#     smtp_connection.close()

#     with smtplib.SMTP('smpt.gmail.com', 587, timeout=5) as smtp_connection:
#         yield smtp_connection


# @pytest.fixture(scope='module')
# def smtp_connection(request):
#     smtp_connection = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)

#     def fin():
#         print('teardown smtp_connection')
#         smtp_connection.close()

#     request.addfinalizer(fin)
#     return smtp_connection


# @pytest.fixture(scope='module')
# def smtp_connection(request):
#     server = getattr(request.module, 'smtp_server', 'smtp.gmail.com')
#     smtp_connection = smtplib.SMTP(server, 587, timeout=5)
#     yield smtp_connection
#     print('finalizing {} ({})'.format(smtp_connection, server))
#     smtp_connection.close()


@pytest.fixture(scope='module', params=['smtp.gmail.com', 'mail.python.org'])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print('finalizing {}'.format(smtp_connection))
    smtp_connection.close()

import pytest


@pytest.fixture
def smtp_connection():
    import smtplib
    return smtplib.SMTP('smtp.gmail.com', 587, timeout=5)


def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()

    assert response == 250
    assert 0  # for demo purpose

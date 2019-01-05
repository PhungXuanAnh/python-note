import pytest


@pytest.fixture(scope='module', params=['mod1', 'mod2'])
def modarg(request):
    param = request.param
    print(' setup modarg {}'.format(param))
    yield param
    print(' TEARDOWN modarg {}'.format(param))


@pytest.fixture(scope='function', params=[1,2])
def otherarg(request):
    param = request.param
    print(' SETUP otherarg {}'.format(param))
    yield param
    print(' TEARDOWN otherarg {}'.format(param))


def test_0(otherarg):
    print(' RUN test0 with otherarg {}'.format(otherarg))


def test_1(modarg):
    print(' RUN test1 with modarg {}'.format(modarg))    


def test_2(otherarg, modarg):
    print( 'RUN test2 with otherarg {} and modarg {}'.format(otherarg, modarg))

    
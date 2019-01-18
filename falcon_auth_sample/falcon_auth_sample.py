import falcon
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend, TokenAuthBackend


def user_loader(username, password):
    return {'username': username}


auth_backend = BasicAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(auth_backend)

api = falcon.API(middleware=[auth_middleware])


class ApiResourceBasicAuth:

    def on_post(self, req, resp):
        user = req.context['user']
        resp.body = 'User Found: {}'.format(user['username'])

    # def on_get(self, req, resp):
    #     resp.body = "This is resource doesn't need authentication"


class ApiResourceTokenAuth:

    auth = {
        'backend': TokenAuthBackend(user_loader=lambda token: {'id': 'token123'}),
        'exempt_methods': ['GET']
    }

    # def on_post(self, req, resp):
    #     user = req.context['user']
    #     resp.body = 'User Found: {}'.format(user['username'])

    # token auth backend
    def on_post(self, req, resp):
        resp.body = "This is resource uses token authentication"

    def on_get(self, req, resp):
        resp.body = "This is resource doesn't need authentication"


api.add_route('/api_token_auth', ApiResourceTokenAuth())
api.add_route('/api_basic_auth', ApiResourceTokenAuth())

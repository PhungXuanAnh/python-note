import redis


class LuaRedisClient(redis.Redis):

    def __init__(self, *args, **kargs):
        super(LuaRedisClient, self).__init__(*args, **kargs)
        for name, snippet in self._get_lua_funcs():
            self._create_lua_method(name, snippet)

    def _get_lua_funcs(self):
        """
            Return name/snippet pair for earch lua function in the atoms.lua file
        """
        with open('lua-scripts/atoms.lua', 'r') as f:
            for func in f.read().strip().split('function '):
                if func:
                    bits = func.split('\n', 1)
                    name = bits[0].split('(')[0].strip()
                    snippet = bits[1].rsplit('end', 1)[0].strip()
                    yield name, snippet

    def _create_lua_method(self, name, snippet):
        """
            Registers the code snippet as a Lua script, and binds the script to the
            client as a method that can be called with the same signature as regular
            client methods, eg with a single key arg.
        """
        script = self.register_script(snippet)
        # method = lambda key, *a, **k: script(keys=[key], args=a, **k)

        def method(key, *a, **k):
            return script(keys=[key], args=a, **k)

        setattr(self, name, method)

if __name__ == '__main__':
    client = LuaRedisClient()
    client.rpush("key", "foo", "bar", "baz")
    print(client.list_pop("key", 1))
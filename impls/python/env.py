
class Env:

    def __init__(self, outer_env, binds = [], exprs = []):
        self.data = {}
        self.outer = outer_env
        for key, value in zip(binds, exprs):
            self.set(key, value)

    def set(self, symbol_key, mal_value):
        """ set: takes a symbol key and a mal value and adds to the data structure
        """
        self.data[symbol_key] = mal_value

    def find(self, symbol_key):
        """ find: takes a symbol key and if the current environment contains that key
        then return the environment. If no key is found and outer is not nil then call
        find (recurse) on the outer environment.
        """
        if symbol_key in self.data:
            return self
        elif self.outer:
            return self.outer.find(symbol_key)
        else:
            return None

    def get(self, symbol_key):
        """ get: takes a symbol key and uses the find method to locate the environment
        with the key, then returns the matching value. If no key is found up the outer
        chain, then throws/raises a "not found" error.
        """
        # print('symbol: '+str(symbol_key))
        # print('env '+str(self.data))
        if symbol_key in self.data:
            return self.data[symbol_key]

        environment = self.find(symbol_key)
        print('outer-env '+str(environment))

        if environment:
            return environment.get(symbol_key)

        raise Exception(str(symbol_key) + " not found")

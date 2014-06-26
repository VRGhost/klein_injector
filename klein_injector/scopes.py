import injector

import werkzeug.local

class CachedProviderWrapper(injector.Provider):
    """
    (This class is shamelessly inspired by the RequestScope of flask-injector)
    """

    def __init__(self, old_provider):
        super(CachedProviderWrapper, self).__init__()
        self._old_provider = old_provider
        self._cache = {}

    def get(self, injector):
        key = id(injector)
        try:
            return self._cache[key]
        except KeyError:
            instance = self._cache[key] = self._old_provider.get(injector)
            return instance

class RequestScope(injector.Scope):
    """A scope whose lifetime is tied to a request.

    (This class is shamelessly inspired by the RequestScope of flask-injector)
    """

    def configure(self):
        self._locals = werkzeug.local.Local()
        self._local_manager = werkzeug.local.LocalManager([self._locals])
        self.reset()

    def reset(self):
        self._local_manager.cleanup()
        self._locals.scope = {}

    def get(self, key, provider):
        try:
            return self._locals.scope[key]
        except KeyError:
            new_provider = CachedProviderWrapper(provider)
            self._locals.scope[key] = new_provider
            return new_provider

request = injector.ScopeDecorator(RequestScope)
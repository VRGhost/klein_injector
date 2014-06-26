import functools

import injector

from . import scopes

class KleinInjector(object):
    """Main extension object that tailors together injector and Klein"""

    app = injector = None

    def __init__(self, app, injector):
        """
            Arguments:
                `app` - `klein.Klein` class injstance.
                `injector` - injector object to be used.
        """
        self.app = app
        self.injector = injector
        self.activate()

    def activate(self):
        """Install injector into Kleins' call handler."""
        self.injector.binder.bind_scope(scopes.RequestScope)
        self._oldAppCall = self.app._call
        self.app._call = self._appMonkeyPatchCall

    def _appMonkeyPatchCall(self, instance, func, *args, **kwargs):

        @functools.wraps(func)
        def _funcWithInjection(*fArgs, **fKwargs):
            if instance is not None:
                assert fArgs[0] is instance
                fArgs = fArgs[1:]

            self.injector.get(scopes.RequestScope).reset()

            return self.injector.call_with_injection(
                func, self_=instance,
                args=fArgs, kwargs=fKwargs
            )

        return self._oldAppCall(
            instance, _funcWithInjection,
            *args, **kwargs
        )
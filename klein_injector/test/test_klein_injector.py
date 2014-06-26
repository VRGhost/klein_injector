import injector
import mock

import klein
import klein.ext

from twisted.trial import unittest
from twisted.internet.defer import inlineCallbacks

from klein.resource import KleinResource
from klein.test.test_resource import requestMock, _render

class KleinInjectorTestCase(unittest.TestCase):

    def test_ext_module_loaded(self):
        """Test that klein extension mechanism loaded klein_injector library."""

        self.assertTrue(hasattr(klein.ext, "injector"))
        import klein_injector
        self.assertIs(klein.ext.injector, klein_injector)

    @inlineCallbacks
    def test_basic_injection(self):
        TEST_MSG = "Hello world from injector!"

        def configure(binder):
            binder.bind(str, to=TEST_MSG)

        inj = injector.Injector([configure])
        app = klein.Klein()
        klein.ext.injector.KleinInjector(app, inj)

        @app.route("/")
        @injector.inject(injectedParam=str)
        def test_handler(request, injectedParam):
            return injectedParam

        request = requestMock('/')
        kr = KleinResource(app)
        yield _render(kr, request)
        self.assertEqual(request.getWrittenData(), TEST_MSG)

    @inlineCallbacks
    def test_double_injection(self):
        msg1 = "Hello world from injector!"
        msg2 = ("hello", "word")

        def configure(binder):
            binder.bind(str, to=msg1)
            binder.bind(tuple, to=msg2)

        inj = injector.Injector([configure])
        app = klein.Klein()
        kr = KleinResource(app)
        klein.ext.injector.KleinInjector(app, inj)

        @app.route("/")
        @injector.inject(p1=str, p2=tuple)
        def test_handler(request, p1, p2):
            return "-".join((p1, ) + p2)

        request = requestMock('/')
        yield _render(kr, request)

        self.assertEqual(
            request.getWrittenData(),
            "-".join((msg1,) + msg2)
        )

    @inlineCallbacks
    def test_request_scope_successive_calls(self):
        callee = mock.Mock()

        def configure(binder):
            binder.bind(object, to=lambda: callee(),
                scope=klein.ext.injector.request
            )

        inj = injector.Injector([configure])
        app = klein.Klein()
        kr = KleinResource(app)
        klein.ext.injector.KleinInjector(app, inj)

        @app.route("/")
        @injector.inject(p1=object)
        def test_handler(request, p1):
            return "Hello"

        @app.route("/page2")
        @injector.inject(p1=object)
        def test_handler(request, p1):
            return "Hello"

        yield _render(kr, requestMock('/'))
        yield _render(kr, requestMock('/'))
        yield _render(kr, requestMock('/page2'))

        self.assertEqual(callee.call_count, 3)

    @inlineCallbacks
    def test_request_scope_sub_calls(self):

        callee = mock.Mock()

        def configure(binder):
            binder.bind(object, to=lambda: callee(),
                scope=klein.ext.injector.request
            )

        inj = injector.Injector([configure])
        app = klein.Klein()
        kr = KleinResource(app)
        klein.ext.injector.KleinInjector(app, inj)

        @injector.inject(arg=object)
        def handler_dep_dep(arg):
            return True

        @injector.inject(arg=object, depDep=handler_dep_dep)
        def handler_dep(arg, depDep):
            return True

        @app.route("/")
        @injector.inject(p1=object, depRv=handler_dep)
        def test_handler(request, p1, depRv):
            return "Hello"

        yield _render(kr, requestMock('/'))
        self.assertEqual(callee.call_count, 1)
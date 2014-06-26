============================
Klein-Injector, a binding between Klein and Injector
============================


Example
=======

The below example will output "Hello world!" as "/" page

.. code-block:: python

    import injector
    import klein
    import klein.ext

    app = klein.Klein()

    @app.route("/")
    @injector.inject(injectedParam=str)
    def test_handler(request, injectedParam):
        return injectedParam

    def configure(binder):
        binder.bind(str, to="Hello World!")

    inj = injector.Injector([configure])

    klein.ext.injector.KleinInjector(app, inj)
    app.run()

You can also use `klein.ext.injector.request` scope in your bindings.

.. code-block:: python
    def configure(binder):
        binder.bind(str, to="A long time ago in a galaxy far, far away",
            scope=klein.ext.injector.request
        )
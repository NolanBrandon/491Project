## ✅ Test Results - Thu Oct  9 20:04:07 UTC 2025


==================================== ERRORS ====================================
___________________ ERROR collecting test_api_performance.py ___________________
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/runner.py:341: in from_call
    result: Optional[TResult] = func()
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/runner.py:372: in <lambda>
    call = CallInfo.from_call(lambda: list(collector.collect()), "collect")
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/python.py:531: in collect
    self._inject_setup_module_fixture()
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/python.py:545: in _inject_setup_module_fixture
    self.obj, ("setUpModule", "setup_module")
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/python.py:310: in obj
    self._obj = obj = self._getobj()
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/python.py:528: in _getobj
    return self._importtestmodule()
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/python.py:617: in _importtestmodule
    mod = import_path(self.path, mode=importmode, root=self.config.rootpath)
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/pathlib.py:567: in import_path
    importlib.import_module(module_name)
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:186: in exec_module
    exec(co, module.__dict__)
test_api_performance.py:3: in <module>
    from rest_framework.test import APIClient
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/rest_framework/test.py:139: in <module>
    class APIRequestFactory(DjangoRequestFactory):
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/rest_framework/test.py:140: in APIRequestFactory
    renderer_classes_list = api_settings.TEST_REQUEST_RENDERER_CLASSES
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/rest_framework/settings.py:218: in __getattr__
    val = self.user_settings[attr]
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/rest_framework/settings.py:209: in user_settings
    self._user_settings = getattr(settings, 'REST_FRAMEWORK', {})
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/django/conf/__init__.py:102: in __getattr__
    self._setup(name)
/opt/hostedtoolcache/Python/3.12.11/x64/lib/python3.12/site-packages/django/conf/__init__.py:82: in _setup
    raise ImproperlyConfigured(
E   django.core.exceptions.ImproperlyConfigured: Requested setting REST_FRAMEWORK, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
=========================== short test summary info ============================
ERROR test_api_performance.py - django.core.exceptions.ImproperlyConfigured: Requested setting REST_FRAMEWORK, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
2 warnings, 1 error in 0.85s


# Test Results - 2025-10-09 20:21:45

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-09 20:21:45\n

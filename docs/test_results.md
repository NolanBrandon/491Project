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

# Test Results - 2025-10-09 21:13:20

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-09 21:13:20\n

# Test Results - 2025-10-09 23:09:58

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-09 23:09:58\n

# Test Results - 2025-10-09 23:16:44

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-09 23:16:44\n

# Test Results - 2025-10-09 23:21:45

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-09 23:21:45\n

# Test Results - 2025-10-09 23:26:46

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0

# Test Results - 2025-10-10 02:01:12

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 02:01:12\n

# Test Results - 2025-10-10 02:03:17

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 02:03:17\n

# Test Results - 2025-10-10 22:17:09

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 22:17:09\n

# Test Results - 2025-10-10 22:22:29

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 22:22:29\n

# Test Results - 2025-10-10 22:26:26

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 22:26:26\n

# Test Results - 2025-10-10 22:30:43

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 22:30:43\n

# Test Results - 2025-10-10 22:34:42

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 22:34:42\n

# Test Results - 2025-10-10 22:55:30

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-10 22:55:30\n

# Test Results - 2025-10-11 21:53:56

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-11 21:53:56\n

# Test Results - 2025-10-11 22:18:08

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-11 22:18:08\n

# Test Results - 2025-10-12 00:45:25

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 00:45:25\n

# Test Results - 2025-10-12 00:46:11

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 00:46:11\n

# Test Results - 2025-10-12 01:40:13

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 01:40:13\n

# Test Results - 2025-10-12 01:41:48

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 01:41:48\n

# Test Results - 2025-10-12 20:12:47

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 20:12:47\n

# Test Results - 2025-10-12 21:15:36

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 21:15:35\n

# Test Results - 2025-10-13 22:23:19

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-13 22:23:19\n
\n# CI Run: 2025-10-12 08:12:23\n

# Test Results - 2025-10-12 20:38:42

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 20:38:42\n

# Test Results - 2025-10-12 21:09:22

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-12 21:09:22\n

# Test Results - 2025-10-14 02:07:12

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-14 02:07:12\n

# Test Results - 2025-10-14 02:09:25

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-14 02:09:25\n

# Test Results - 2025-10-14 02:12:48

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-14 02:12:48\n

# Test Results - 2025-10-16 05:03:19

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-16 05:03:19\n

# Test Results - 2025-10-17 01:19:30

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-17 01:19:30\n

# Test Results - 2025-10-19 05:07:01
# Test Results - 2025-10-17 01:21:30

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-19 05:07:01\n

# Test Results - 2025-10-19 05:09:30
\n# CI Run: 2025-10-17 01:21:30\n

# Test Results - 2025-10-17 01:37:27

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-19 05:09:30\n

# Test Results - 2025-10-19 06:19:21
\n# CI Run: 2025-10-17 01:37:27\n

# Test Results - 2025-10-17 01:49:29

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-19 06:19:21\n

# Test Results - 2025-10-19 06:48:18
\n# CI Run: 2025-10-17 01:49:29\n

# Test Results - 2025-10-17 01:50:09

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-19 06:48:18\n
\n# CI Run: 2025-10-17 01:50:09\n

# Test Results - 2025-10-19 04:10:48

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-19 04:10:48\n

# Test Results - 2025-10-19 07:16:05
# Test Results - 2025-10-19 06:50:17

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-19 07:16:05\n
\n# CI Run: 2025-10-19 06:50:17\n

# Test Results - 2025-10-20 02:10:50

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-20 02:10:50\n

# Test Results - 2025-10-20 03:36:01

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-10-20 03:36:01\n

# Test Results - 2025-11-12 18:18:57

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-12 18:18:57\n

# Test Results - 2025-11-13 00:45:00

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-13 00:45:00\n

# Test Results - 2025-11-13 00:46:39

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-13 00:46:39\n

# Test Results - 2025-11-13 04:41:21

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-13 04:41:21\n

# Test Results - 2025-11-15 02:05:53

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-15 02:05:53\n

# Test Results - 2025-11-16 00:44:13

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-16 00:44:13\n

# Test Results - 2025-11-16 00:45:48

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-16 00:45:48\n

# Test Results - 2025-11-16 00:46:56

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-16 00:46:56\n

# Test Results - 2025-11-17 04:44:44

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-17 04:44:44\n

# Test Results - 2025-11-17 04:46:38

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-17 04:46:38\n

# Test Results - 2025-11-17 04:54:22

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-17 04:54:22\n

# Test Results - 2025-11-17 07:18:46

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-17 07:18:46\n

# Test Results - 2025-11-17 07:25:38

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-17 07:25:38\n

# Test Results - 2025-11-17 07:31:00

- Total tests: 0
- Failures: 0
- Errors: 0
- Skipped: 0
\n# CI Run: 2025-11-17 07:31:00\n

# pytest-pubsubit

[![PyPI version][]][1]

[![Python versions][]][1]

[![See Build Status on Travis CI][]][2]

[![See Build Status on AppVeyor][]][3]

PubSub Integration Test in Python

## Features

-   Easy integration test
-   Session/Class/Function level fixtures

## Requirements

-   google-cloud-pubsub

## Installation

You can install "pytest-pubsubit" via [pip][] from [PyPI][]:

    $ pip install pytest-pubsubit

## Setup

This pluging uses pytest.ini or the option that passes to the pytest
to configure the PubSub emulator and also find the path to 
the global fixtures.

A sample pytest.ini:
```
[pytest]
testpaths =
    tests/integration
pubsubit_project=test-project
pubsubit_topics_subscriptions={"test-topic":["test-subscription","test-subscription-1"],"test-topic-2":["test-subscription-2","test-subscription-3"]}
pubsubit_global_fixtures_path=tests/integration/fixtures/pubsub
```
Or command line option:
```
--pubsubit-project test-project
...
```


## Usage

This plugin contains different fixtures to help setup and 
teardown the Pub/Sub. Each of these will put 
the Pub/Sub in a proper state for the test function.

- psm_session_fixture:
- psm_class_fixture:
- psm_function_fixture:


## Contributing

Contributions are very welcome. Tests can be run with [tox][], please
ensure the coverage at least stays the same before you submit a pull
request.

## License

Distributed under the terms of the [MIT][] license, "pytest-pubsubit" is
free and open source software

## Issues

If you encounter any problems, please [file an issue][] along with a
detailed description.

  [PyPI version]: https://img.shields.io/pypi/v/pytest-pubsubit.svg
  [1]: https://pypi.org/project/pytest-pubsubit
  [Python versions]: https://img.shields.io/pypi/pyversions/pytest-pubsubit.svg
  [See Build Status on Travis CI]: https://travis-ci.org/mahyar-m/pytest-pubsubit.svg?branch=master
  [2]: https://travis-ci.org/mahyar-m/pytest-pubsubit
  [See Build Status on AppVeyor]: https://ci.appveyor.com/api/projects/status/github/mahyar-m/pytest-pubsubit?branch=master
  [3]: https://ci.appveyor.com/project/mahyar-m/pytest-pubsubit/branch/master
  [pytest]: https://github.com/pytest-dev/pytest
  [Cookiecutter]: https://github.com/audreyr/cookiecutter
  [@hackebrot]: https://github.com/hackebrot
  [cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
  [pip]: https://pypi.org/project/pip/
  [PyPI]: https://pypi.org/project
  [tox]: https://tox.readthedocs.io/en/latest/
  [MIT]: http://opensource.org/licenses/MIT
  [file an issue]: https://github.com/mahyar-m/pytest-pubsubit/issues
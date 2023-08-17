import os

pytest_plugins = [
    "src.pytest_pubsubit.plugin",
]

os.environ['PUBSUB_EMULATOR_HOST'] = '127.0.0.1:8085'
os.environ['PUBSUB_PROJECT_ID'] = 'test-project'

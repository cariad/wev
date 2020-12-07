from os import environ
print(f'Hello, {environ.get("DEMO_NAME", "whoever you are")}!')

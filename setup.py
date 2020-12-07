from pathlib import Path

from setuptools import setup

from wev.version import get_version

readme_path = Path(__file__).parent.joinpath("README.md")

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Internet",
    "Topic :: Security",
    "Topic :: Utilities",
]

version = get_version()

if "a" in version:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in version:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.me",
    classifiers=classifiers,
    description="Run shell commands with environment variables",
    entry_points={
        "console_scripts": [
            "wev=wev.__main__:cli_entry",
        ],
        "wev.plugins": "wev-echo = wev.wev_echo",
    },
    include_package_data=True,
    install_requires=[
        "colorama~=0.4",
        "dwalk~=1.1",
        "pytz",
        "ruamel.yaml~=0.16",
    ],
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="wev",
    packages=[
        "wev",
        "wev.logging",
        "wev.sdk",
        "wev.state",
        "wev.text",
    ],
    # "py.typed" in each package's directory must be included for the package to
    # be considered typed.
    package_data={
        "wev": ["py.typed"],
        "wev.logging": ["py.typed"],
        "wev.sdk": ["py.typed"],
        "wev.state": ["py.typed"],
        "wev.text": ["py.typed"],
    },
    python_requires=">=3.8",
    url="https://github.com/cariad/wev",
    version=version,
)

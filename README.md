# wev: run shell commands with environment variables

**This is prerelease software. Don't use it. :)**

`wev` is a command line tool for resolving environment variables then running shell commands.

For example:

- If you have a `Pipfile` that expects the `CODEARTIFACT_AUTH_TOKEN` environment variable to set, `wev pipenv install` can resolve the value then run `pipenv install`.
- If your AWS IAM user demands multi-factor authentication, `wev aws s3 ls` can prompt for your token, resolve `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN`, then run `aws s3 ls`.

## Installation

`wev` requires Python 3.8 or later.

```bash
pip3 install wev
```

You will also need to install the plugins that you intend to use. For example, to enable AWS MFA support:

```bash
pip3 install wev-awsmfa
```

## Configuration

### File locations

`wev` is configured via `.wev.yml` files.

`wev` will look for and merge `.wev.yml` files in this order:

1. `.wev.yml` in your home directory. This is the ideal place for environment variables you _always_ need.
1. All `.wev.yml` files between the volume root and your current working directory.

If multiple `.wev.yml` files are found then they will be merged. The `.wev.yml` file in your home directory has the lowest precedence, while your working directory has the highest.

### File contents

Each `.wev.yml` is a dictionary, where the _key_ is the name of the environment variable to set and the _value_ is the plugin identifier and configuration:

```yaml
ENVIRONMENT_VARIABLE_NAME:
  plugin:
    id: PLUGIN_NAME
    PLUGIN_CONFIGURATION_KEY: PLUGIN_CONFIGURATION_VALUE
    PLUGIN_CONFIGURATION_KEY: PLUGIN_CONFIGURATION_VALUE
    PLUGIN_CONFIGURATION_KEY: PLUGIN_CONFIGURATION_VALUE
```

For example, to configure the `wev-echo` plugin (bundled with `wev`) to resolve the environment variable `USERNAME` to the hard-coded value `Finn Mertens`:

```yaml
USERNAME:
  plugin:
    id: wev-echo
    value: Finn Mertens
```

If a plugin resolves multiple environment variables--such as `pip-awsmfa`--then the names are specified as a list:

```yaml
[AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN]:
  plugin:
    id: wev-awsmfa
```

## Command line usage

To get help:

```bash
wev
wev --help
```

To see an explanation of what `wev` is planning to do:

```bash
wev --explain
```

To resolve environment variables and run a shell command:

```bash
wev <command goes here>
# For example:
wev pipenv install
```

## Demo

1. Install `wev`.
1. Clone or download this project.
1. `cd` into the `demo` directory.

Inside `demo` are two files:

1. A `.wev.yml` configuration file that will set the `DEMO_NAME` environment variable to `Finn Mertens`.
1. `hello.py`, which will greet you by the name set in the `DEMO_NAME` environment variable.

First, run the script directly:

```bash
python hello.py
```

```text
Hello, whoever you are!
```

Now, run the script via `wev`:

```bash
wev python hello.py
```

```text
Hello, Finn Mertens!
```

Any example with static, hard-coded values will be contrived, but hopefully this gives you a taste of what's possible with more-complex plugins.

## Plugin development

This documentation is `TODO`. Yell if you want to build a plugin and need a hand.

## Thanks!

My name is [Cariad Eccleston](https://cariad.me) and I'm a freelance DevOps engineer. I love AWS and Python, and I'm available for interesing gigs. Let's chat!

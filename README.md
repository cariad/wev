# corf: A CodeArtifact Orthoriser

`corf` is an AWS CodeArtifact orthorisation… uh I mean _authorisation_ helper for `pipenv` and any other command line tools that read CodeArtifact authorisation tokens as environment variables.

## Introduction

Say you have a `Pipfile` that describes an AWS CodeArtifact repository as a source and an environment variable to hold the authorisation token:

```text
[[source]]
name = "private-pypackages"
url = "https://aws:$CODEARTIFACT_AUTH_TOKEN@starkindustries-012345678901.d.codeartifact.us-east-1.amazonaws.com/pypi/project-ultron/simple"
verify_ssl = true
```

Traditionally, you'd set your authorization token twice a day by running:

```bash
export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token --domain starkindustries --domain-owner 012345678901 --query authorizationToken --output text --region us-east-1)
```

But what if you're a fan of PowerShell or some other weird/wonderful shell? What if you don't want to maintain a set of helper scripts for your team's diverse development machines?

`corf` replaces this:

```bash
# Magic goes here.
pipenv install --dev
```

…with this:

```bash
corf pipenv install
```

## Installation

`corf` requires >= Python 3.8.

### Installing globally

```bash
pip3 install corf
```

### Installing in a virtual environment

`corf` is happy to be installed via `pipenv`:

```bash
pipenv install corf
```

If your `Pipfile` has _only_ private sources that require authorisation tokens then you can add a handy-dandy shortcut script to pull `corf` from the public PyPI index:

```text
[scripts]
get-corf = "pip install --upgrade corf -i https://pypi.python.org/simple"
```

To install `corf` via that shortcut:

```bash
pipenv shell
pipenv run get-corf
```

If your private repository mirrors the public PyPI index and you put `corf` into your `Pipfile` dependencies then you'll need to run `get-corf` only once. Any subsequent runs of `corf pipenv install` will include updates to `corf` itself.

## Configuration

`corf` will walk your directories to find configuration files that describe the environment variables to set and the CodeArtifact domains to request authorisation tokens from.

For example, to request an authorisation token from the "starkindustries" domain in region "eu-west-1" of AWS account "012345678901" and set it to the "AUTH_TOKEN_FOO" environment variable, you could create this `.corf.yml` in your project directory:

```yaml
variables:
  AUTH_TOKEN_FOO:
    domain:
      account: "012345678901"
      name: starkindustries
      region: eu-west-1
```

To run `pipenv install` with the "AUTH_TOKEN_FOO" environment variable set, run:

```bash
corf pipenv install
```

## Named profiles

`corf` will use your default AWS credentials without prompting. If you need to use a specific named profile then you have three options:

1. Run `corf` with the `--profile` option:

```bash
corf --profile corp pipenv install
```

This sucks, though, because you need to remember to add the option.

2. Add a `profile` property to `.corf.yml`:

```yaml
variables:
  AUTH_TOKEN_FOO:
    domain:
      account: "012345678901"
      name: starkindustries
      region: eu-west-1
      profile: corp
```

This sucks, though, if you want to commit `.corf.yml` to source control to share with your team. They likely don't all use the same named profile as you.

3. Create a `.corf.user.yml` file that contains your personal details, and don't commit that file to source control.

So, if `.corf.yml` is:

```yaml
variables:
  AUTH_TOKEN_FOO:
    domain:
      account: "012345678901"
      name: starkindustries
      region: eu-west-1
```

…and if `.corf.user.yml` is:

```yaml
variables:
  AUTH_TOKEN_FOO:
    domain:
      profile: corp
```

…then the two configurations will be merged at runtime.

## Configuration file locations

`corf` will merge all of the configurations that it finds.

In any given directory, `.corf.user.yml` takes precedence over `.corf.yml`.

The current working directory will take precedence, down to the root directory, then finally your home directory.

## Development notes

### Testing

```bash
./lint.sh && ./coverage.sh && ./build.sh
```

## Thanks!

My name is [Cariad Eccleston](https://cariad.me) and I'm a freelance DevOps engineer. I appreciate you checking out my projects! I love AWS and Python, I'm available for interesing gigs, and I'd love to hear from you!

## FAQs

### Why `corf`?

I _really_ wanted to call it `cauth`, but that's a reserved name on pypi.org. `corf` is close enough.

### Should `.corf.yml` be committed to source control?

`.corf.yml`, yes.

`.corf.user.yml`, no.

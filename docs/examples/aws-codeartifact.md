# Amazon Web Services CodeArtifact authorisation token

## Using your default credentials

You're a software developer working on a Python project in `~/foo`. The project is version-controlled in Git, and you work with several other developers.

The project's `Pipfile` references a private package repository hosted in an Amazon Web Service's CodeArtifact domain:

```text
[[source]]
name = "private"
url = "https://aws:$CODEARTIFACT_AUTH_TOKEN@corp-012345678901.d.codeartifact.eu-west-1.amazonaws.com/pypi/pypi-mirror/simple/"
verify_ssl = true
```

Currently, you need to remember to set the `CODEARTIFACT_AUTH_TOKEN` environment variable to a new CodeArtifact authorisation token every twelve hours.

`wev`'s contextual environment variables can manage that for you.

1. Install `wev` and `wev-awscodeartifact`:

    ```bash
    pip3 install wev
    pip3 install wev-awscodeartifact
    ```

1. Create `~/foo/wev.yml`:

    ```yaml
    CODEARTIFACT_AUTH_TOKEN:
      plugin:
        id: wev-awscodeartifact
        domain: corp
    ```

1. Run `pipenv install` via `wev`:

    ```bash
    wev pipenv install
    ```

1. `CODEARTIFACT_AUTH_TOKEN` will be resolved using your default AWS credentials, and your packages will be pulled.
1. `~/foo/wev.yml` can be commited to your code repository and shared with your team.

## Using a personal named profile

Your default AWS named profile holds credentials for a different AWS account.

You _really_ want to use your `work` named profile to generate a CodeArtifact authorisation token, but if you add that configuration to `wev.yml` then _everyone_ in your team will be configured to use that same profile.

`wev`'s contextual environment variables can keep some parts of your configuration private.

1. Create `~/foo/wev.user.yml`:

    ```yaml
    CODEARTIFACT_AUTH_TOKEN:
      plugin:
        profile: work
    ```

1. Run `pipenv install` via `wev`:

    ```bash
    wev pipenv install
    ```

1. The configuration in `wev.yml` and `wev.user.yml` will be merged. `CODEARTIFACT_AUTH_TOKEN` will be resolved using the credentials in your `work` namned profile, and your packages will be pulled.
1. `~/foo/wev.user.yml` should _not_ be commited to your code repository or shared with your team.

# wev-awsmfa

## Overview

`wev-awsmfa` adds support for Amazon Web Services multi-factor authentication.

The source code is on GitHub at [cariad/wev-awsmfa](https://github.com/cariad/wev-awsmfa).

## Installation

```python
pip3 install wev-awsmfa
```

## Configuration

### Keys

`wev-awsmfa` must be configured to resolve _three_ environment variables:

1. The AWS access key ID. You likely want this to be `AWS_ACCESS_KEY_ID`.
1. The AWS secret key. You likely want this to be `AWS_SECRET_ACCESS_KEY`.
1. The AWS session token. You likely want this to be `AWS_SESSION_TOKEN`.

### Properties

| Property   | Required | Description                                   | Default                                   |
|------------|----------|-----------------------------------------------|-------------------------------------------|
| duration   | ⨯        | Duration of the temporary session in seconds. | 900                                       |
| mfa_device | ⨯        | ARN of the multi-factor device to use.        | _Will attempt to discover automatically._ |

## Example

Say you're a software developer working for a client who gave you an IAM user that requires multi-factor authentication.

All of your work for this client is in subdirectories of `~/client-foo`.

You'd like to run the `aws` CLI, but you can't pass one-time tokens to it to authenticate. `wev` can help.

1. Install `wev` and `wev-awsmfa`:

    ```bash
    pip3 install wev
    pip3 install wev-awsmfa
    ```

1. Create `~/client-foo/wev.yml`:

    ```yaml
    [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN]:
      plugin:
        id: wev-awsmfa
    ```

1. `cd` into a project directory, then run `aws` via `wev`:

    ```bash
    cd ~/client-foo/project-bar
    wev aws s3 ls
    ```

1. You will be prompted to enter your one-time token, then `aws` will run.

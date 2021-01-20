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

## Examples

- [Amazon Web Services multi-factor authentication on the command line](/examples/awsmfa)

# wev-echo

## Overview

`wev-echo` resolves to hard-coded values.

## Installation

`wev-echo` is bundled with `wev`.

## Configuration

| Property | Required | Description          |
|----------|----------|----------------------|
| value  | ✔️        | Value to resolve to. |

## Examples

### Amazon Web Services profile

Say you're a freelance software developer.

You have two directories on your develpment machine:

- `~/code` for personal projects.
- `~/client-foo` for client _foo_'s projects.

Both of these projects use Amazon Web Services, and you use the `aws` application daily whether you're working on personal or client projects.

You have AWS named profiles set up for each of these areas:

- The `personal` profile holds credentials for your personal Amazon Web Services account.
- The `foo` profile holds credentials for client _foo_'s Amazon Web Services account.

Right now, you need to remember to run `aws` with `--profile personal` or `--profile foo` depending on the project you're working on. `wev` can help.

1. Install `wev`:

    ```bash
    pip3 install wev
    ```

2. Create `~/code/wev.yml`:

    ```yaml
    AWS_DEFAULT_PROFILE:
      plugin:
        id: wev-echo
        value: personal
    ```

3. Create `~/client-foo/wev.yml`:

    ```yaml
    AWS_DEFAULT_PROFILE:
      plugin:
        id: wev-echo
        value: foo
    ```

4. Open a terminal and `cd` into `~/code`. Verify that the _personal_ named profile is used:

    ```bash
    cd ~/code
    wev aws sts get-caller-identity
    ```

    ```json
    {
      "UserId": "000000000000",
      "Account": "000000000000",
      "Arn": "arn:aws:iam::000000000000:user/personal-you"
    }
    ```

4. Open a terminal and `cd` into `~/client-foo`. Verify that the _foo_ named profile is used:

    ```bash
    cd ~/client-foo
    wev aws sts get-caller-identity
    ```

    ```json
    {
      "UserId": "111111111111",
      "Account": "111111111111",
      "Arn": "arn:aws:iam::111111111111:user/professional-you"
    }
    ```

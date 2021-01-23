# Amazon Web Services named profile per project

You're a freelance software developer. You have two directories to distinguish between your personal and client projects:

- `~/code` for personal projects.
- `~/client-foo` for client _foo_'s projects.

You use Amazon Web Services for both personal and client projects, and you have AWS named profiles set up for each account you interact with:

- The `personal` profile for your personal AWS account.
- The `foo` profile for client _foo_'s AWS account.

Right now, you need to remember to run `aws` with `--profile personal` or `--profile foo` depending on the project you're working on.

However, `wev`'s contextual environment variables can manage that for you.

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
      "Arn": "arn:aws:iam::000000000000:user/you"
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
      "Arn": "arn:aws:iam::111111111111:user/contractor"
    }
    ```

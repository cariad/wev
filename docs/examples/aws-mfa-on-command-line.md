# Amazon Web Services multi-factor authentication on the command line

You're a software developer working for a client who gave you an IAM user that requires multi-factor authentication.

All of your work for this client is in subdirectories of `~/client-foo`.

You'd like to run the `aws` CLI, but you can't pass one-time tokens to it to authenticate.

`wev`'s contextual environment variables can manage that for you.

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

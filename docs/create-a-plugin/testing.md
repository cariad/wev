Create a `wev.yml` configuration file suitable for your plugin:

```yaml
# Invoke the wev-ask plugin to set the DEFAULT_FOO environment variable:
DEFAULT_FOO:
  plugin:
    id: wev-ask

# Invoke the wev-ask plugin to set the LOWER_FOO environment variable:
LOWER_FOO:
  plugin:
    id: wev-ask
    force_case: lower

# Invoke the wev-ask plugin to set the UPPER_FOO environment variable:
UPPER_FOO:
  plugin:
    id: wev-ask
    force_case: upper
```

Install your plugin:

```bash
pipenv install . --skip-lock
```

Verify the plugin is installed by generating an execution plan:

```bash
wev --explain
```

!!! warning
    If you get an error about your plugin not being installed then you're probably running a global installation of `wev` rather than the one in your virtual environment.

    Either uninstall the global installation, or install your plugin globally.

```text
wev (1.1.1) execution plan generated at 2021-01-17 13:44:41:

 1. DEFAULT_FOO will be resolved by the wev-ask plugin.

    You will be prompted to enter a special value, which will be cached for 30 seconds.

 2. LOWER_FOO will be resolved by the wev-ask plugin.

    You will be prompted to enter a special value, which will be cached for 30 seconds.
    Your value will be returned as lower-case.

 3. UPPER_FOO will be resolved by the wev-ask plugin.

    You will be prompted to enter a special value, which will be cached for 30 seconds.
    Your value will be returned as upper-case.
```

Now let's try it!

For this example, I'll assume you're developing in macOS or Linux and have `env` installed to print environment variables:

```bash
wev env
```

You'll be prompted three times to enter a value. Enter `Foo` each time.

Finally, `env` will output your environment variables, and you should see these three:

```text
DEFAULT_FOO=Foo
LOWER_FOO=foo
UPPER_FOO=FOO
```

To verify the caching, run `wev env` again within 30 seconds. This time, you should see `env` run directly without being prompted for values.

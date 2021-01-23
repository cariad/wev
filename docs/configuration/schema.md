# Schema

`wev` configuration files are YAML dictionaries.

## Keys

Each key is the name (or names) of the environment variable (or variables) to set.

It must be either a string or a list, depending on whether the plugin resolves one or more than one value.

## Values

Each value is a `plugin` property which describes the `id` of the plugin in invoke and any plugin-specific configuration.

## Examples

### Single environment variable

This example configures `wev` to resolve `MY_NAME` by invoking the `wev-echo` plugin, with `wev-echo` configured to return "Bobby Pringles".

```yaml
MY_NAME:
  plugin:
    id: wev-echo
    value: Bobby Pringles
```

### Multiple environment variables by multiple plugins

This example configures `wev` to:

1. Resolve `MY_NAME` by invoking the `wev-echo` plugin, with `wev-echo` configured to return "Bobby Pringles".
1. Resolve `MY_ADDRESS` by invoking the `wev-echo` plugin, with `wev-echo` configured to return "Pringland".

```yaml
MY_NAME:
  plugin:
    id: wev-echo
    value: Bobby Pringles

MY_ADDRESS:
  plugin:
    id: wev-echo
    value: Pringland
```

### Multiple environment variables by one plugin

The [wev-awsmfa](https://github.com/cariad/wev-awsmfa) plugin creates temporary Amazon Web Services sessions, which are described by three values: a key identifier, a secret and a session token.

To configure plugins that resolve multiple values, the _key_ must be a _list_.

This example configures `wev` to resolve `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` by invoking the `wev-awsmfa` plugin, with `wev-awsmfa` configured to cache the resulting session for 30 seconds.

```yaml
[AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN]:
  plugin:
    id: wev-awsmfa
    duration: 30
```

Each plugin's own documentation will describe whether the key must be a string or a list.

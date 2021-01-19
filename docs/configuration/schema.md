# Schema

`wev` configurations are dictionaries descibed as YAML.

## Keys

Each _key_ is the name(s) of the environment variable(s) to set.

It must be either a _string_ or a _list_, depending on whether the plugin resolves _one_ or _more than one_ value.

## Values

Each _value_ is a `plugin` property which describes the `id` of the plugin in invoke and any plugin-specific configuration.

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

The [wev-awsmfa](/plugins/wev-awsmfa.md) plugin creates temporary Amazon Web Services sessions, which are described by three values: a key identifier, a secret and a session token.

To configure plugins that resolve multiple values, the _key_ must be a _list_.

This example configures `wev` to resolve `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` by invoking the `wev-awsmfa` plugin, with `wev-awsmfa` configured to cache the resulting session for 30 seconds.

```yaml
[AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN]:
  plugin:
    id: wev-awsmfa
    duration: 30
```

Each plugin's own documentation will describe whether the _key_ must be a _string_ or a _list_.

# Directories

`wev` is contextual.

Running `wev` from two different working directories could result in different environment variables being resolved, or the same environment variables being resolved in different ways.

To achieve this, the [placement](directories.md) of [configuration files](schema.md) is significant.

## Precedence

`wev` reads and merges configuration files in the following order:

1. The working directory.
1. The parent directory, and parents up to the root.
1. Your home directory.

To be clear, any `wev` configuration in your home directory will _always_ be loaded, but could be overridden by higher-precedence configuration.

## Merging of different environment variables.

Say these two configuration files exist:

- `~/example/wev.yml`
- `~/wev.yml`

```yaml
# ~/example/wev.yml
MY_FORENAME:
  plugin:
    id: wev-echo
    value: Bobby
```

```yaml
# ~/wev.yml
MY_SURNAME:
  plugin:
    id: wev-echo
    value: Pringles
```

When running from `~/example`, `wev` would set `MY_FORENAME=Bobby` and `MY_SURNAME=Pringles`. The configurations for `MY_FORENAME` and `MY_SURNAME` are merged side-by-side.

When running from `~/`, only `MY_SURNAME=Pringles` would be set. `wev` seeks configuration files in parent directories, and never in child directories.

## Merging of configurations for the same environment variable

Say these two configuration files exist:

- `~/example/wev.yml`
- `~/wev.yml`

```yaml
# ~/example/wev.yml
MY_NAME:
  plugin:
    id: wev-echo
    separator: "_"
```

```yaml
# ~/wev.yml
MY_NAME:
  plugin:
    id: wev-echo
    separator: "-"
    value:
      - Bobby
      - Pringles
```

When running from `~/example`, `wev` would set `MY_NAME=Bobby_Pringles`. The configuration in this directory overrides the configuration in lower directories.

When running from `~/`, `MY_NAME=Bobby-Pringles` would be set.

## Configuration properties are never merged


Say these two configuration files exist:

- `~/example/wev.yml`
- `~/wev.yml`

```yaml
# ~/example/wev.yml
MY_NAME:
  plugin:
    id: wev-echo
    value:
      - Kim
      - Disco
```

```yaml
# ~/wev.yml
MY_NAME:
  plugin:
    id: wev-echo
    value:
      - Bobby
      - Pringles
```

When running from `~/example`, `wev` would set `MY_NAME=Kim Disco`.

When running from `~/`, `MY_NAME=Bobby Pringles` would be set.

The list items of `value`--or _any_ primitive configuration property--are never merged.

# Filenames

`wev` supports both shareable and private configuration.

To achieve this, the naming of [configuration files](../schema) is significant.

## Precedence

`wev` will seek and merge these configuration files, in order of least- to highest-precedence:

1. `.wev.yml`
1. `wev.yml`
1. `.wev.user.yml`
1. `wev.user.yml`

To be clear, a `wev.user.yml` in any given directory will override anyt configuration in `wev.yml` in the same directory.

## Team vs user configuration

The dotted vs not-dotted files (i.e. `.wev.yml` vs `wev.yml`) are provided for your own preference. Some folks like dots, others don't.

`wev.yml` files are intended to be committed to version control and shared, while `wev.user.yml` are intended to hold personal configurations.

## Merging of different environment variables.

Say these two configuration files exist:

- `~/wev.user.yml`
- `~/wev.yml`

```yaml
# ~/wev.user.yml
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

When running from `~`, `wev` would set `MY_FORENAME=Bobby` and `MY_SURNAME=Pringles`. The configurations for `MY_FORENAME` and `MY_SURNAME` are merged side-by-side.

## Merging of configurations for the same environment variable

Say these two configuration files exist:

- `~/wev.user.yml`
- `~/wev.yml`

```yaml
# ~/wev.user.yml
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

When running from `~`, `wev` would set `MY_NAME=Bobby_Pringles`. The configuration in `wev.user.yml` overrides the configuration in `wev.yml`.

## Configuration properties are never merged

Say these two configuration files exist:

- `~/wev.user.yml`
- `~/wev.yml`

```yaml
# ~/wev.user.yml
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

When running from `~`, `wev` would set `MY_NAME=Kim Disco`.

The list items of `value`--or _any_ primitive configuration property--are never merged.

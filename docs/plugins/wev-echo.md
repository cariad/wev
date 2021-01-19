# wev-echo

`wev-echo`

```yaml
MY_NAME:
  plugin:
    id: wev-echo
    value: Bobby Pringles
```


The `wev-echo` plugin is bundled with `wev` and doesn't need to be installed separately.


## Examples

### Amazon Web Services profile name

Say you're a freelance software developer.

You have two directories on your develpment machine:

- `~/code` for personal projects.
- `~/client-foo` for client _foo_'s projects.

Both of these projects use Amazon Web Services, and you use the `aws` application daily whther you're working on personal or client projects.

You have AWS named profiles set up for each of these areas:

- The `personal` profile holds credentials for your personal Amazon Web Services account.
- The `foo` profile holds credentials for client _foo_'s Amazon Web Services account.

Right now, you need to remember to run `aws` with `--profile personal` or `--profile foo` depending on the project you're working on. `wev` can help.

Create `~/code/.wev.yml`:

```yaml
AWS_DEFAULT_PROFILE:
  plugin:
    id: wev-echo
    value: personal
```

Create `~/client-foo/.wev.yml`:

```yaml
AWS_DEFAULT_PROFILE:
  plugin:
    id: wev-echo
    value: foo
```

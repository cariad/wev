This guide won't go into `setup.py` in detail.

The only detail specific to plugin development is that you must add an entry point to `wev.plugins` which points your plugin name to its package.

In this example, the plugin's name is `wev-ask` and the package name is `wev_ask`:

```python
setup(
    # ...
    entry_points={
        "wev.plugins": "wev-ask = wev_ask",
    },
    # ...
)
```

# Directories

`wev` is contextual.

Running `wev` from two different working directories could result in different environment variables being resolved, or the same environment variables being resolved in different ways.

To achieve this, the [placement](directories.md) of [configuration files](schema.md) is significant.

## Precedence

`wev` reads and merges condfiguration files in the following order:

1. The working directory.
1. The parent directory, and parents up to the root.
1. Your home directory.

To be clear, any `wev` configuration in your home directory will _always_ be loaded, but could be overridden by higher-precedence configuration.

## Merging

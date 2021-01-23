# wev: with environment variables

`wev` is a cross-platform command line tool for resolving temporary environment variables.

For example:

- `wev` can [create a multi-factor authenticated Amazon Web Services session](/examples/awsmfa).
<!-- - `wev` can [request a CodeArtifact authorisation token on behalf of pipenv](/examples/awscodeartifact.md). -->

In a nutshell:

- ⚙️ Extensible via **[plugins](/plugins)**.
- 👷‍♀️ **[Create your own plugins](/create-a-plugin)** to suit any need.
- 🔎 **[Contextual](/configuration/directories)**. Resolve different environment variables in different working directories.
- 🔎 **[Team and private](/configuration/filenames)** configurations live side-by-side.
- 📋 **Caches** values to avoid delays and prompts.

# Introduction

A `wev` plugin is simply a Python package that exposes a class that inherits and implements `wev.sdk.PluginBase`.

In this example, We're going to create a plugin named `wev-ask`. This plugin will prompt users to enter a value, and cache it for 30 seconds.

I'll be using `pipenv` to manage my Python virtual environments, but naturally feel free to reject my preferences and substitute your own.

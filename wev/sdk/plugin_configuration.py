class PluginConfiguration(dict):
    @property
    def id(self) -> str:
        return str(self["id"])

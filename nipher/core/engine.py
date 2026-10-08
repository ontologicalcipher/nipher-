from importlib import import_module

class Engine:
    MODULES = {
        "domain": "nipher.modules.domain",
        "web": "nipher.modules.web",
        "network": "nipher.modules.network",
        "username": "nipher.modules.username",
        "metadata": "nipher.modules.metadata",
        "youtube": "nipher.modules.youtube",
        "satellite": "nipher.modules.satellite",
        "geoint": "nipher.modules.geoint",
    }

    def run(self, module: str, target: str, **kwargs):
        if module not in self.MODULES:
            raise ValueError(f"Unknown module: {module}")

        mod = import_module(self.MODULES[module])

        if not hasattr(mod, "run"):
            raise RuntimeError(f"Module '{module}' has no run() function")

        return mod.run(target, **kwargs)

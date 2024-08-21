import os

import yaml


class Bot:
    @staticmethod
    def from_dir(d):
        with open(os.path.join(d, "manifest.yaml"), "r") as fp:
            manifest = yaml.safe_load(fp)
        return Bot(d, **manifest)

    def __init__(self, d, **kwargs):
        if not d:
            raise ValueError("d is required")
        cloud = kwargs.get("cloud")
        if not cloud:
            raise ValueError("cloud is required")
        cloud = cloud.strip().lower()
        entry_point = None
        python = kwargs.get("python")
        if python:
            entry_point = python.get("entrypoint")
        entry_point = entry_point if entry_point else "bot"
        self.cloud = cloud
        parts = entry_point.split("#", maxsplit=1)
        self.module_dir = d
        self.module_name = parts[0]
        self.function_name = parts[1] if len(parts) > 1 else "run"

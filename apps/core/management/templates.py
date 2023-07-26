import os
from functools import cached_property
from pathlib import Path

from django.conf import settings


class BaseTemplate:
    files = []

    def __init__(
        self,
        parent_directory: Path | None = None,
        root: Path | None = None,
        ignore_parent=False,
    ):
        self.ignore_parent = ignore_parent
        self.parent_directory = parent_directory or ""
        self.root = root or ""

    @cached_property
    def directories(self):
        if not self.parent_directory and self.ignore_parent is False:
            raise TypeError(
                "You must either provide a `parent_directory` or set `ignore_parent` to True"
            )

        return [
            (
                self.parent_directory / self.root / "/".join(file.split("/")[:-1]),
                file.split("/")[-1],
            )
            for file in self.files
        ]

    @cached_property
    def write_only_directories(self):
        if not self.parent_directory and self.ignore_parent is False:
            raise TypeError(
                "You must either provide a `parent_directory` or set `ignore_parent` to True"
            )

        return [
            (
                settings.BASE_DIR / "/".join(file.split("/")[:-1]),
                file.split("/")[-1],
            )
            for file in self.files
        ]

    def make_template(self):
        try:
            os.mkdir(self.parent_directory / self.root)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"No such app in directory '{self.parent_directory}'"
            ) from exc
        except FileExistsError as exc:
            raise FileExistsError(
                f"The api in already setup in directory: '{self.parent_directory}'"
            ) from exc

        for directory in self.directories:
            directory = tuple(map(str, directory))
            print(directory)
            self.make_parent_directories(directory[0])
            try:
                print("/".join(directory))
                os.mknod("/".join(directory))
            except FileExistsError:
                pass
        self.write_data()
        self.extra_write()

    def extra_write(self):
        ...

    def make_parent_directories(self, directory: str):
        directory = directory.split("/")
        for idx, _ in enumerate(directory):
            try:
                os.mkdir("/".join(directory[: idx + 1]) + "/")
            except FileExistsError:
                continue

    def write_data(self):
        for directory in self.directories:
            attr_name = f"{directory[1].replace('/', '_').replace('.py', '')}_write"
            if hasattr(self, attr_name):
                attr = getattr(self, attr_name)
                self.perform_write(attr, directory[0] / directory[1])

    def perform_write(self, function, directory):
        function(directory)

    def append_file(self, file_path: str, data: str, overwrite=False):
        with open(f"{file_path}", "r+", encoding="utf-8") as file:
            if overwrite:
                file_data = file.read()
                if data not in file_data:
                    file.write(f"\n{data}")
            else:
                file.write(data)

    def write_file(self, file_path: str, data: str):
        with open(f"{file_path}", "w", encoding="utf-8") as file:
            file.write(data)

    def replace_file(self, file_path: str, data: list):
        with open(f"{file_path}", "r+", encoding="utf-8") as file:
            file_data = file.read()
            replace_data = data

            if not isinstance(data, list):
                raise TypeError(
                    "data must be instance of list containing tuples which represent new and old values"
                )

            for i in replace_data:
                file_data = file_data.replace(*i)

            file.truncate()
            file.seek(0)
            file.write(file_data)


class ApiTemplate(BaseTemplate):
    files = ["views.py", "serializers.py", "urls.py"]
    ROOT = "api"

    def views_write(self, file):
        self.write_file(file, "from rest_framework.viewsets import ModelViewSet")

    def extra_write(self):
        self.append_file(
            os.path.join(settings.BASE_DIR, "requirements/base.txt"),
            "djangorestframework==3.13.1",
            True,
        )

from setuptools import setup

PROJECT_URL = {
    "Issues": "https://github.com/Mojitaba34/alert-winglet/issues",
    "Source Code": "https://github.com/Mojitaba34/alert-winglet",
}

setup(
    setup_cfg=True,
    py_modules=[],
    package_dir={"": "apps"},
    project_urls=PROJECT_URL,
    packages=["alert_winglet"],
)

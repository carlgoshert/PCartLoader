import tomllib

def main():
    version = ""
    with open("pyproject.toml", "rb") as f:
        project = tomllib.load(f)["project"]
        with open("src/_version.py", "w") as f:
            f.write(f'__version__ = "{project["version"]}"\n')
            version = project["version"]
    return version
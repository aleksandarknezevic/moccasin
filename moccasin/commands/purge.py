import subprocess
from argparse import Namespace

from packaging.requirements import Requirement

from moccasin._dependency_helpers import get_base_install_path
from moccasin.config import get_config
from moccasin.logging import logger


def main(args: Namespace):
    _purge(args.packages, args.quiet)


def _purge(packages: list[str], quiet: bool = False):
    path = get_base_install_path()
    cmd = ["uv", "pip", "uninstall", *packages, "--target", str(path)]

    capture_output = quiet
    subprocess.run(cmd, capture_output=capture_output, check=True)

    config = get_config()
    dependencies = config.get_dependencies()

    to_delete = set()
    for package in packages:
        for dep in dependencies:
            if Requirement(dep).name == Requirement(package).name:
                to_delete.add(dep)
        logger.info(f"Removed {package}")

    dependencies = [dep for dep in dependencies if dep not in to_delete]
    config.write_dependencies(dependencies)

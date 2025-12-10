"""Generate requirements.txt from installed packages."""

import argparse
import sys
from importlib.metadata import distributions
from typing import List, Dict, Set, Optional


def get_installed_packages(exclude_editable: bool = False) -> List[Dict[str, str]]:
    """Get list of installed packages with their versions using importlib.metadata."""
    packages = []
    for dist in distributions():
        try:
            # Skip editables if requested
            if exclude_editable and not dist.files:
                continue

            # Get package name and version
            pkg_name = dist.metadata["Name"]
            if not pkg_name:  # Skip if no name
                continue

            # Normalize package name to match pip's behavior
            pkg_name = pkg_name.replace("_", "-").lower()

            packages.append({"name": pkg_name, "version": dist.version})
        except Exception as e:
            metadata = dist.metadata.get("Name", "unknown")
            print(
                f"Warning: Could not process package {metadata}: {e}",
                file=sys.stderr,
            )

    return packages


def format_requirement(pkg: Dict[str, str], format_spec: str = "pip") -> str:
    """Format package information according to the specified format."""
    if format_spec == "pip":
        return f"{pkg['name']}=={pkg['version']}"
    elif format_spec == "conda":
        return f"{pkg['name']}={pkg['version']}"
    return f"{pkg['name']}=={pkg['version']}"


def generate_requirements(
    output_file: str = "requirements.txt",
    exclude_editable: bool = False,
    format_spec: str = "pip",
    exclude_packages: Optional[Set[str]] = None,
) -> None:
    """Generate requirements file from installed packages."""
    if exclude_packages is None:
        exclude_packages = set()

    try:
        packages = get_installed_packages(exclude_editable)

        with open(output_file, "w", encoding="utf-8") as f:
            for pkg in sorted(packages, key=lambda x: x["name"].lower()):
                if pkg["name"].lower() not in exclude_packages:
                    f.write(format_requirement(pkg, format_spec) + "\n")

        print(f"Successfully generated {output_file} with {len(packages)} packages.")
    except Exception as e:
        print(f"Error generating requirements file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Generate requirements.txt from installed packages."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="requirements.txt",
        help="Output file path (default: requirements.txt)",
    )
    parser.add_argument(
        "--exclude-editable",
        action="store_true",
        help="Exclude packages installed in editable mode",
    )
    parser.add_argument(
        "--format",
        choices=["pip", "conda"],
        default="pip",
        help="Output format (default: pip)",
    )
    parser.add_argument(
        "--exclude", nargs="+", default=[], help="Packages to exclude from the output"
    )

    args = parser.parse_args()

    generate_requirements(
        output_file=args.output,
        exclude_editable=args.exclude_editable,
        format_spec=args.format,
        exclude_packages={pkg.lower() for pkg in args.exclude},
    )


if __name__ == "__main__":
    main()

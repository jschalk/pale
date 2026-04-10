from pathlib import Path
from src.ch00_py.file_toolbox import create_path, open_json
from src.ch17_idea.idea_config import get_brick_formats_dir, get_default_sorted_list


def get_brick_md(brick_config) -> str:
    # Create per-idea Markdown file
    idea = brick_config["brick_type"]
    attr_names = set(brick_config["attributes"].keys())
    dimens = list(brick_config["dimens"])
    sorted_attrs = get_default_sorted_list(attr_names)

    idea_md_lines = [
        f"# Idea `{idea}`\n",
        f"## Dimens `{dimens}`\n",
        "## Attributes",
        *(f"- `{attr}`" for attr in sorted_attrs),
    ]
    return "\n".join(idea_md_lines) + "\n"


def get_brick_mds(brick_format_dir: str = None) -> dict[str,]:
    if not brick_format_dir:
        brick_format_dir = get_brick_formats_dir()

    brick_formats_dir = Path(brick_format_dir)
    brick_mds = {}
    for json_path in sorted(brick_formats_dir.glob("*.json")):
        brick_format = open_json(json_path)
        brick_type = brick_format["brick_type"]
        brick_mds[brick_type] = get_brick_md(brick_format)

    return brick_mds


def get_brick_formats_md():
    brick_formats_dir = Path(get_brick_formats_dir())

    manifest_lines = []
    for json_path in sorted(brick_formats_dir.glob("*.json")):
        data = open_json(json_path)

        idea = data["brick_type"]
        attr_names = set(data["attributes"].keys())
        sorted_attrs = get_default_sorted_list(attr_names)
        idea_md_path = create_path("brick_formats", f"{idea}.md")
        manifest_line = f"- [`{idea}`]({idea_md_path}): " + ", ".join(sorted_attrs)
        manifest_lines.append(manifest_line)

    # Where the Markdown manifest will be written
    return "# Idea Manifest\n\n" + "\n".join(manifest_lines)

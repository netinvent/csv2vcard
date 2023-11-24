import os


def export_vcard(vcard: str, output_dir: str, filename: str):
    """
    Exporting a vCard to /export/
    """
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(vcard)
            fh.close()
            print(f"Created vCard for {filename}.")
    except OSError as exc:
        print(f"Could not write file {filepath}: {exc}")


def check_export_dir(output_dir: str) -> None:
    """
    Checks if export folder exists in directory
    """
    if not os.path.exists(output_dir):
        print(f"Creating {output_dir} folder...")
        os.makedirs(output_dir)

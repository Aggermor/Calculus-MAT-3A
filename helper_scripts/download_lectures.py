import csv
import re
import subprocess
import sys
from pathlib import Path


def clean_filename(name: str) -> str:
    """Remove characters that Windows does not allow in file/folder names."""
    name = str(name).strip()
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", " ", name)
    return name[:140]


def normalize_row(row: dict) -> dict:
    """Strip spaces from CSV headers and values."""
    return {
        str(key).strip(): str(value).strip()
        for key, value in row.items()
        if key is not None and value is not None
    }


def main() -> None:
    csv_path = Path("videos.csv")

    if len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])

    if not csv_path.exists():
        print(f"Could not find {csv_path}")
        print("Create a videos.csv file first, or pass the CSV path as an argument.")
        sys.exit(1)

    base_output = Path("lectures")
    archive_file = Path("downloaded-lectures.txt")
    failed_rows = []
    markdown_links = []

    # Prefer MP4/M4A, then fall back to best available.
    format_selector = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/best"

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        required_columns = {"module", "section", "title", "url"}
        fieldnames = {str(name).strip() for name in (reader.fieldnames or [])}
        missing = required_columns - fieldnames

        if missing:
            print(f"CSV is missing columns: {', '.join(sorted(missing))}")
            print(f"Found columns: {', '.join(sorted(fieldnames))}")
            sys.exit(1)

        for raw_row in reader:
            row = normalize_row(raw_row)

            if not any(row.values()):
                continue

            module = clean_filename(row.get("module", ""))
            section = clean_filename(row.get("section", ""))
            title = clean_filename(row.get("title", ""))
            url = row.get("url", "").strip()

            if not all([module, section, title, url]):
                print(f"Skipping incomplete row: {row}")
                continue

            folder = base_output / f"module-{module}"
            folder.mkdir(parents=True, exist_ok=True)

            final_mp4 = folder / f"{section} - {title}.mp4"
            output_template = str(folder / f"{section} - {title}.%(ext)s")

            markdown_path = final_mp4.as_posix()
            markdown_links.append(
                f"- Module {module}, {section} — [{title}]({markdown_path})"
            )

            if final_mp4.exists():
                print(f"Already exists, skipping: {final_mp4}")
                continue

            print()
            print(f"Downloading Module {module}, Section {section}: {title}")

            command = [
                sys.executable,
                "-m", "yt_dlp",
                "-f", format_selector,
                "--merge-output-format", "mp4",
                "--embed-metadata",
                "--continue",
                "--no-overwrites",
                "--retries", "infinite",
                "--fragment-retries", "infinite",
                "--download-archive", str(archive_file),
                "-o", output_template,
                url,
            ]

            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError:
                print(f"FAILED: Module {module}, Section {section}: {title}")
                failed_rows.append([module, section, title, url])
                continue

    Path("generated-lecture-links.md").write_text(
        "# Generated Lecture Links\n\n" + "\n".join(markdown_links) + "\n",
        encoding="utf-8",
    )

    if failed_rows:
        failed_path = Path("failed-downloads.csv")
        with failed_path.open("w", encoding="utf-8", newline="") as failed_file:
            writer = csv.writer(failed_file)
            writer.writerow(["module", "section", "title", "url"])
            writer.writerows(failed_rows)

        print()
        print(f"Done, but {len(failed_rows)} download(s) failed.")
        print(f"Failed rows written to {failed_path}")
    else:
        print()
        print("Done. No failed downloads.")

    print("Lecture links written to generated-lecture-links.md")


if __name__ == "__main__":
    main()
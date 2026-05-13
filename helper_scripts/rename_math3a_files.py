from pathlib import Path
import argparse
import sys


# Hardcoded renames from the original downloaded filenames to clean study-map filenames.
# Notes files become: "section_number section_name Notes.pdf"
# Other files from the same section become: "section_number section_name Extra.pdf", "Extra2", etc.
RENAMES = [
    # 2.1 Secant Lines and Velocity
    ("Math 3A Section 2.1 Notes.pdf", "2.1 Secant Lines and Velocity Notes.pdf"),
    ("Math 3A Section 2.1 (2).pdf", "2.1 Secant Lines and Velocity Extra.pdf"),

    # 2.2 Limits of a Function
    ("Math 3A Section 2.2 Notes.pdf", "2.2 Limits of a Function Notes.pdf"),
    ("Math 3A section 2.2.pdf", "2.2 Limits of a Function Extra.pdf"),

    # 2.3 Calculating Limits
    ("Math 3A Section 2.3 Notes.pdf", "2.3 Calculating Limits Notes.pdf"),
    ("Math 3A Section 2.3.pdf", "2.3 Calculating Limits Extra.pdf"),

    # 2.5 Continuity
    ("Math 3A Section 2.5 Notes.pdf", "2.5 Continuity Notes.pdf"),
    ("Math 3A Section 2.5 (1).pdf", "2.5 Continuity Extra.pdf"),

    # 2.6 Limits Involving Infinity
    ("Math 3A Section 2.6 Notes.pdf", "2.6 Limits Involving Infinity Notes.pdf"),
    ("Math 3A Section 2.6 (2).pdf", "2.6 Limits Involving Infinity Extra.pdf"),

    # 2.7 Derivatives as Rates of Change
    ("Math 3A Section 2.7 Notes.pdf", "2.7 Derivatives as Rates of Change Notes.pdf"),
    ("Math 3A Section 2.7.pdf", "2.7 Derivatives as Rates of Change Extra.pdf"),

    # 2.8 Derivative as a Function
    ("Math 3A Section 2.8 Notes.pdf", "2.8 Derivative as a Function Notes.pdf"),
    ("Math 3A Section 2.8.pdf", "2.8 Derivative as a Function Extra.pdf"),

    # 3.1 The Power Rule
    ("Math 3A Section 3.1 Notes.pdf", "3.1 The Power Rule Notes.pdf"),
    ("Math 3A Section 3.1 (1).pdf", "3.1 The Power Rule Extra.pdf"),

    # 3.2 Product and Quotient Rules
    ("Math 3A Section 3.2 Notes.pdf", "3.2 Product and Quotient Rules Notes.pdf"),
    ("Math 3A Section 3.2.pdf", "3.2 Product and Quotient Rules Extra.pdf"),

    # 3.3 Derivatives of Trig Functions
    ("Math 3A Section 3.3 Notes.pdf", "3.3 Derivatives of Trig Functions Notes.pdf"),
    ("Math 3A Section 3.3.pdf", "3.3 Derivatives of Trig Functions Extra.pdf"),

    # 3.4 The Chain Rule
    ("Math 3A Section 3.4 Notes.pdf", "3.4 The Chain Rule Notes.pdf"),
    ("Math 3A Section 3.4 .pdf", "3.4 The Chain Rule Extra.pdf"),

    # 3.5 Implicit Differentiation
    ("Math 3A Section 3.5 Notes Part 2.pdf", "3.5 Implicit Differentiation Notes.pdf"),
    ("Math 3A Section 3.5.pdf", "3.5 Implicit Differentiation Extra.pdf"),

    # 3.6 Logarithmic Differentiation
    ("Math 3A Section 3.6 Notes.pdf", "3.6 Logarithmic Differentiation Notes.pdf"),
    ("Math 3A Section 3.6.pdf", "3.6 Logarithmic Differentiation Extra.pdf"),

    # 3.7 Derivatives as Rates of Change
    ("Math 3A Section 3.7 Notes.pdf", "3.7 Derivatives as Rates of Change Notes.pdf"),
    ("Math 3A Section 3.7 (1).pdf", "3.7 Derivatives as Rates of Change Extra.pdf"),

    # 3.9 Related Rates
    ("Math 3A Section 3.9 Notes.pdf", "3.9 Related Rates Notes.pdf"),
    ("Math 3A Section 3.9.pdf", "3.9 Related Rates Extra.pdf"),

    # 3.10 Linear Approximations
    ("Math 3A Section 3.10 Notes.pdf", "3.10 Linear Approximations Notes.pdf"),
    ("Math 3A Section 3.10.pdf", "3.10 Linear Approximations Extra.pdf"),

    # 4.1 Minimums and Maximums
    ("Math 3A Section 4.1 Notes.pdf", "4.1 Minimums and Maximums Notes.pdf"),
    ("Math 3A Section 4.1.pdf", "4.1 Minimums and Maximums Extra.pdf"),

    # 4.2 The Mean Value Theorem
    ("Math 3A Section 4.2 Notes.pdf", "4.2 The Mean Value Theorem Notes.pdf"),
    ("Math 3A Section 4.2.pdf", "4.2 The Mean Value Theorem Extra.pdf"),

    # 4.3 Derivatives and Graphing
    ("Math 3A Section 4.3 Notes.pdf", "4.3 Derivatives and Graphing Notes.pdf"),
    ("Math 3A Section 4.3.pdf", "4.3 Derivatives and Graphing Extra.pdf"),

    # 4.4 L'Hopital's Rule
    ("Math 3A Section 4.4 Notes.pdf", "4.4 L'Hopital's Rule Notes.pdf"),
    ("Math 3A Section 4.4 l’Hospital’s Rule.pdf", "4.4 L'Hopital's Rule Extra.pdf"),

    # 4.7 Optimization
    ("Math 3A Section 4.7 Notes.pdf", "4.7 Optimization Notes.pdf"),
    ("Math 3A Section 4.7.pdf", "4.7 Optimization Extra.pdf"),

    # 4.8 Newton's Method
    ("Math 3A Section 4.8 Notes.pdf", "4.8 Newton's Method Notes.pdf"),
    ("Math 3A Section 4.8.pdf", "4.8 Newton's Method Extra.pdf"),

    # 4.9 Integration
    ("Math 3A Section 4.9 Notes.pdf", "4.9 Integration Notes.pdf"),
    ("Math 3A Section 4.9.pdf", "4.9 Integration Extra.pdf"),

    # 5.1 Riemann Sums
    ("Math 3A Section 5.1 Notes.pdf", "5.1 Riemann Sums Notes.pdf"),
    ("Math 3A Section 5.1 (1).pdf", "5.1 Riemann Sums Extra.pdf"),
    ("Section 5.1 Lower Sum.jpg", "5.1 Riemann Sums Extra2.jpg"),
    ("Section 5.1 Upper Sum.jpeg", "5.1 Riemann Sums Extra3.jpeg"),

    # 5.2 The Definite Integral
    ("Math 3A Section 5.2 Notes.pdf", "5.2 The Definite Integral Notes.pdf"),
    ("Math 3A Section 5.2.pdf", "5.2 The Definite Integral Extra.pdf"),

    # 5.3 Fundamental Theorem of Calculus
    ("Math 3A Section 5.3 Notes.pdf", "5.3 Fundamental Theorem of Calculus Notes.pdf"),
    ("Math 3A Section 5.3.pdf", "5.3 Fundamental Theorem of Calculus Extra.pdf"),

    # 5.4 Definite vs Indefinite Integrals
    ("Math 3A Section 5.4 Notes.pdf", "5.4 Definite vs Indefinite Integrals Notes.pdf"),
    ("Math 3A Section 5.4.pdf", "5.4 Definite vs Indefinite Integrals Extra.pdf"),

    # 5.5 U-substitution
    ("Math 3A Section 5.5 Notes.pdf", "5.5 U-substitution Notes.pdf"),
    ("Math 3A Section 5.5.pdf", "5.5 U-substitution Extra.pdf"),

    # 6.1 Area Between Curves
    ("Math 3A Section 6.1 Notes.pdf", "6.1 Area Between Curves Notes.pdf"),
    ("Math 3A Section 6.1.pdf", "6.1 Area Between Curves Extra.pdf"),

    # 6.2 Solids of Revolution
    ("Math 3A Section 6.2 Notes.pdf", "6.2 Solids of Revolution Notes.pdf"),
    ("Math 3A Section 6.2.pdf", "6.2 Solids of Revolution Extra.pdf"),
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Hardcoded renamer for Math 3A downloaded note/example files."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder containing the files. Defaults to the current folder.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files. Without this, the script only previews changes.",
    )
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()

    if not folder.exists():
        print(f"Folder does not exist: {folder}")
        sys.exit(1)

    print(f"Folder: {folder}")
    print("Mode:", "APPLY / RENAME FILES" if args.apply else "DRY RUN / PREVIEW ONLY")
    print()

    missing = []
    skipped_existing = []
    renamed = []

    # Check for duplicate target names in the hardcoded list.
    targets = [target for _, target in RENAMES]
    duplicate_targets = sorted({target for target in targets if targets.count(target) > 1})
    if duplicate_targets:
        print("ERROR: Duplicate target filenames in script:")
        for name in duplicate_targets:
            print(f"  {name}")
        sys.exit(1)

    for old_name, new_name in RENAMES:
        old_path = folder / old_name
        new_path = folder / new_name

        if not old_path.exists():
            missing.append(old_name)
            continue

        if new_path.exists() and old_path != new_path:
            skipped_existing.append((old_name, new_name))
            continue

        print(f"{old_name}")
        print(f"  -> {new_name}")

        if args.apply:
            old_path.rename(new_path)

        renamed.append((old_name, new_name))

    print()
    print(f"Planned/renamed: {len(renamed)}")
    print(f"Missing: {len(missing)}")
    print(f"Skipped because target already exists: {len(skipped_existing)}")

    if missing:
        print()
        print("Missing files:")
        for name in missing:
            print(f"  {name}")

    if skipped_existing:
        print()
        print("Skipped because target already exists:")
        for old_name, new_name in skipped_existing:
            print(f"  {old_name} -> {new_name}")

    if not args.apply:
        print()
        print("This was only a preview. To actually rename files, run again with --apply")


if __name__ == "__main__":
    main()

"""
Count words in a file.
"""

import sys
import re
import os


def analyse_file(filename):
    """Count words in am Italian markdown file."""
    ret = {}
    with open(filename, "r") as file:
        text = file.read().lower()
        # count the number of images
        images = re.findall(r"!\[.*\]\(.*\)", text)
        ret["images"] = len(images)
        words = re.findall(r"\w+", text)
        chars = len(text)
        ret["words"] = len(words)
        ret["chars"] = chars
    return ret


def n_files_to_message(n_files):
    if n_files == 0:
        print("⚠️ Non ci sono file")
    elif n_files <= 2:
        print("❌ Non ci sono abbastanza file")
    elif n_files <= 5:
        print("✅ Numero sufficiente o ottimale di file")
    elif n_files <= 7:
        print("👍👍 Buono! Non ci sono file di troppo")
    elif n_files <= 10:
        print("👍 Ci sono pochi file di troppo")
    elif n_files <= 15:
        print("👎 Ci sono alcuni file di troppo")
    else:
        print("🔥🔥 C'è molto lavoro da fare!")


def n_words_to_message(n_words):
    if n_words < 300:
        cat = "vs"
    elif n_words < 500:
        cat = "short"
    elif n_words < 1000:
        cat = "📝 medium"
    elif n_words < 2000:
        cat = "📝📝 quitelong"
    else:
        cat = "‼️ veeerylooong"
    return cat


def count_words_dir(dirname, recursive=True):
    """
    Count words for each file in a directory, recursively.
    """
    count = 0
    ret = []
    for root, dirs, files in os.walk(dirname):
        if not recursive:
            dirs.clear()

        files = sorted(f for f in files if f[0] != "." and f.endswith(".md"))
        print(f"{len(files):,} files in {root}")

        n_files_to_message(len(files))

        for filename in files:
            if filename.endswith(".md"):
                path = os.path.join(root, filename)
                file_stats = analyse_file(path)
                words = file_stats["words"]
                images = file_stats["images"]
                img_stats = "🖼" if images > 0 else ""
                cat = n_words_to_message(words)
                print(f"{img_stats}\t{words:6,} {cat:13} {path}")
                count += words
                ret.append((words, path))
    ret.sort(reverse=True)
    print(f"{count:6,} total")
    mean = count / len(files)
    print(f"{mean:6.1f} mean")


def main():
    """Run the program."""
    if len(sys.argv) != 2:
        print("Usage: python counter.py <directory>")
        sys.exit(1)
    dirname = sys.argv[1]
    count_words_dir(dirname)


if __name__ == "__main__":
    main()

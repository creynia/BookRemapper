from ruamel import yaml
import argparse

def find_section(book, old_page):
    my_section = None
    for section in book["sections"]:
        if old_page > book["sections"][section]["old-first-page"]:
            if not my_section or my_section["old-first-page"] < book["sections"][section]["old-first-page"]:
                my_section = book["sections"][section]
    return my_section

def calc_new_page(section, old_page):
    # calc offset
    if section:
        offset = section["new-first-page"] - section["old-first-page"]
    else:
        return old_page
    # apply offset
    return old_page + offset

def clear_previous_refs(book, ref):
    book["references"][ref]["new-pages"] = []
    for section in book["sections"]:
        if "new-references" in book["sections"][section]:
            if ref in book["sections"][section]["new-references"]:
                book["sections"][section]["new-references"][ref] = []

def parse_book(path, force_flow):
    if force_flow:
        y = yaml.YAML(typ="safe")
        y.default_flow_style = True
    else:
        y = yaml.YAML()
        y.default_flow_style = None
    with open(path, "r") as f:
        book = y.load(f)
        for ref in book["references"]:
            clear_previous_refs(book, ref)
            for page in book["references"][ref]["old-pages"]:
                section = find_section(book, page)
                new_page = calc_new_page(section, page)
                book["references"][ref]["new-pages"].append(new_page)
                if section:
                    if "new-references" not in section:
                        section["new-references"] = {}
                    if ref not in section["new-references"]:
                        section["new-references"][ref] = []
                    section["new-references"][ref].append(new_page)
    if book:
        with open(path, "w") as f:
            y.dump(book, f)

def print_example(path):
    y = yaml.YAML()
    book = \
        "sections:\n" \
        "  Chapter 1:\n" \
        "    old-first-page: 10\n" \
        "    new-first-page: 10\n" \
        "  Chapter 2:\n" \
        "    old-first-page: 21\n" \
        "    new-first-page: 23\n" \
        "  Chapter 3:\n" \
        "    old-first-page: 28\n" \
        "    new-first-page: 31\n" \
        "references:\n" \
        "  cat:\n" \
        "    old-pages: [9, 11, 22, 29]\n" \
        "  dog:\n" \
        "    old-pages: [2, 15, 50]\n"

    with open(path, "w") as f:
        y.dump(y.load(book), f)


parser = argparse.ArgumentParser(description="Tool for remapping references from one book layout to another. Run with --example to generate a configuration file.")
parser.add_argument("file", help="path to yml file describing book to be remapped")
parser.add_argument("--example", "-e", help="generate example configuration file", action="store_true")
parser.add_argument("--flow", "-f", help="output with less readible 'flow' style", action="store_true")
args = parser.parse_args()
if args.example:
    print_example(args.file)
else:
    parse_book(args.file, args.flow)
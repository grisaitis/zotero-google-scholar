import argparse
import logging
import sys

from .core import (
    add_google_scholar_link_to_item,
    add_google_scholar_links,
    demo,
    has_google_scholar_attachment,
    print_child_items,
    print_collections,
    print_item,
    print_items,
)


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--logging-level", type=str, default="INFO", help="Python logging level"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("demo")
    subparsers.add_parser("print-collections")
    print_items = subparsers.add_parser("print-items")
    print_items.add_argument("collection_key")
    print_item = subparsers.add_parser("print-item")
    print_item.add_argument("item_key")
    print_child_items = subparsers.add_parser("print-child-items")
    print_child_items.add_argument("item_key")
    create_google_scholar_link = subparsers.add_parser(
        "add-google-scholar-link-to-item"
    )
    create_google_scholar_link.add_argument("item_key")
    create_google_scholar_links = subparsers.add_parser("add-google-scholar-links")
    create_google_scholar_links.add_argument("collection_key")
    has_google_scholar_link = subparsers.add_parser("has-google-scholar-link")
    has_google_scholar_link.add_argument("item_key")
    return parser


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=args.logging_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.command == "demo":
        demo()
    elif args.command == "print-collections":
        print_collections()
    elif args.command == "print-items":
        print_items(args.collection_key)
    elif args.command == "print-item":
        print_item(args.item_key)
    elif args.command == "print-child-items":
        print_child_items(args.item_key)
    elif args.command == "add-google-scholar-link-to-item":
        add_google_scholar_link_to_item(args.item_key)
    elif args.command == "add-google-scholar-links":
        add_google_scholar_links(args.collection_key)
    elif args.command == "has-google-scholar-link":
        print(has_google_scholar_attachment(args.item_key))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())

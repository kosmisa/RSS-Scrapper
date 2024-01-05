from xml.etree import ElementTree as Et
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import json as json_module
import requests


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json_output: bool = False,
    json: bool = False
) -> List[str]:
    try:
        root = Et.fromstring(xml)
        channel = root.find(".//channel")

        result = [
            f"Feed: {channel.findtext('title')}",
            f"Link: {channel.findtext('link')}",
            f"Last Build Date: {channel.findtext('lastBuildDate') or None}",
            f"Publish Date: {channel.findtext('pubDate') or None}",
            f"Language: {channel.findtext('language') or None}",
        ]

        categories = channel.findall(".//category")
        if categories:
            result.append("Categories: " +
                          ", ".join(category.text for category in categories))

        result.append(
            f"Managing Editor: {channel.findtext('managingEditor') or None}")
        result.append(
            f"Description: {channel.findtext('description') or None}")

        items = root.findall(".//item")[:limit]
        for item in items:
            result.append("\n")
            result.append(f"Title: {item.findtext('title') or None}")
            result.append(f"Author: {item.findtext('author') or None}")
            result.append(f"Published: {item.findtext('pubDate') or None}")
            result.append(f"Link: {item.findtext('link') or None}")
            result.append(f"Category: {item.findtext('category') or None}")
            result.append(
                f"Description: {item.findtext('description') or None}")

        if json or json_output:
            json_result = {
                "title": channel.findtext('title') or 'None',
                "link": channel.findtext('link') or 'None',
                "lastBuildDate": channel.findtext('lastBuildDate') or None,
                "pubDate": channel.findtext('pubDate') or None,
                "language": channel.findtext('language') or None,
                "category": [category.text for category in categories],
                "managingEditor": channel.findtext('managingEditor') or None,
                "description": channel.findtext('description') or None,
                "items": [
                    {
                        "title": item.findtext('title') or None,
                        "author": item.findtext('author') or None,
                        "pubDate": item.findtext('pubDate') or None,
                        "link": item.findtext('link') or None,
                        "category": item.findtext('category') or None,
                        "description": item.findtext('description') or None,
                        "guid": item.findtext('guid') or None,
                    }
                    for item in items
                ],
            }

            return [json_module.dumps(json_result, indent=2)]
        return result

    except Exception as e:
        raise UnhandledException(e)


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)
    if not args.source:
        print("Error: Please provide an RSS URL.")
        return 1

    try:
        response = requests.get(args.source)
        response.raise_for_status()
        xml = response.text
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()

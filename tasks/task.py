from xml.etree import ElementTree as Et
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import json as json_module


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    try:
        root = Et.fromstring(xml)
        channel = root.find(".//channel")

        result = [
            f"Feed: {channel.findtext('title')}",
            f"Link: {channel.findtext('link')}",
            f"Last Build Date: {channel.findtext('lastBuildDate') or 'None'}",
            f"Publish Date: {channel.findtext('pubDate') or 'None'}",
            f"Language: {channel.findtext('language') or 'None'}",
        ]

        categories = channel.findall(".//category")
        if categories:
            result.append("Categories: " +
                          ", ".join(category.text for category in categories))

        result.append(
            f"Managing Editor: {channel.findtext('managingEditor') or 'None'}")
        result.append(
            f"Description: {channel.findtext('description') or 'None'}")

        items = root.findall(".//item")[:limit]
        for item in items:
            result.append("\n")
            result.append(f"Title: {item.findtext('title') or 'None'}")
            result.append(f"Author: {item.findtext('author') or 'None'}")
            result.append(f"Published: {item.findtext('pubDate') or 'None'}")
            result.append(f"Link: {item.findtext('link') or 'None'}")
            result.append(f"Category: {item.findtext('category') or 'None'}")
            result.append(
                f"Description: {item.findtext('description') or 'None'}")
        return result

    except Exception as e:
        raise UnhandledException(e)

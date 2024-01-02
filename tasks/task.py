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

        return result

    except Exception as e:
        raise UnhandledException(e)

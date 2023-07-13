import re
from typing import Optional


class Tag:
    tag_name: str
    pattern: str
    foreground: str
    background: Optional[str] = "#FFFFFF"
    def __init__(self, tag):
        self.tag_name = tag['tag_name']
        self.pattern = tag['pattern']
        self.foreground = tag['foreground']
        #self.background = tag['background']

class LogTags:
    tags = [
        Tag({"tag_name": "info", "pattern": r'(INFO)', "foreground": 'blue'}),
        Tag({"tag_name": "warning", "pattern": r'(WARNING)', "foreground": 'orange'}),
        Tag({"tag_name": "error", "pattern": r'(ERROR)', "foreground": 'red'}),
        Tag({"tag_name": "time", "pattern": r'\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2}.\d{6}', "foreground": 'grey'}),

    ]

class QueryTags:
    tags = [
        Tag({"tag_name": "property", "pattern": r'(\w+)\s?:', "foreground": 'green'}),
        Tag({"tag_name": "insert", "pattern": r'(\s?insert\s?:)', "foreground": 'blue'}),
        Tag({"tag_name": "update", "pattern": r'(\s?update\s?:)', "foreground": 'orange'}),
        Tag({"tag_name": "delete", "pattern": r'(\s?delete\s?:)', "foreground": 'red'}),
        Tag({"tag_name": "comment", "pattern": r'(#.*)', "foreground": 'gray'}),
    ]


class XMLTags:
    tags = [
        Tag({"tag_name": "element1", "pattern": r'<([^/\s>]+)', "foreground": 'blue'}),
        Tag({"tag_name": "element2", "pattern": r'</([^/\s>]+)>', "foreground": 'blue'}),
        Tag({"tag_name": "attribute", "pattern": r'(\w+)=["\'][^"\']*["\']', "foreground": 'orange'}),
        Tag({"tag_name": "value", "pattern": r'["\']([^"\']*)["\']', "foreground": 'green'}),
        Tag({"tag_name": "comment", "pattern": r'<!--.*-->', "foreground": 'gray'})
    ]


class PropertyTags:
    tags = [
        Tag({"tag_name": "property", "pattern": r'(\w+=)', "foreground": 'blue'}),
        Tag({"tag_name": "value", "pattern": r'(=.*)', "foreground": 'orange'}),
        Tag({"tag_name": "comment", "pattern": r'(#.*)', "foreground": 'gray'}),
    ]


class TextHightlighter:

    def __init__(self, text):
        self.text = text

    def highlight_syntax(self, highlighter):
        xml_content = self.text.get('1.0', 'end')

        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        for tag in highlighter.tags:
            for match in re.finditer(tag.pattern, xml_content):
                start = match.start()
                end = match.end()
                self.text.tag_add(tag.tag_name, f'1.0+{start}c', f'1.0+{end}c')
            self.text.tag_config(tag.tag_name, foreground=tag.foreground)
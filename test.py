from tkinter import *
import re

def highlight_xml_syntax(event):
    xml_content = text.get('1.0', 'end')
    text.tag_remove('tag_comment', '1.0', 'end')
    text.tag_remove('tag_element1', '1.0', 'end')

    text.tag_remove('tag_attribute', '1.0', 'end')
    text.tag_remove('tag_value', '1.0', 'end')

    pattern_comment = r'<!--.*?-->'
    pattern_element1 = r'<([^/\s>]+)'
    pattern_element2 = r'</([^/\s>]+)>'
    pattern_attribute = r'(\w+)=["\'][^"\']*["\']'
    pattern_value = r'["\']([^"\']*)["\']'

    tags = [
        ('tag_comment', pattern_comment),
        ('tag_element1', pattern_element1),
        ('tag_element2', pattern_element2),
        ('tag_attribute', pattern_attribute),
        ('tag_value', pattern_value)
    ]


    for tag_name, pattern in tags:
        for match in re.finditer(pattern, xml_content):
            start = match.start()
            end = match.end()
            text.tag_add(tag_name, f'1.0+{start}c', f'1.0+{end}c')

    text.tag_config('tag_comment', foreground='gray')
    text.tag_config('tag_element1', foreground='blue')
    text.tag_config('tag_element2', foreground='blue')
    text.tag_config('tag_attribute', foreground='red')
    text.tag_config('tag_value', foreground='green')


root = Tk()
text = Text(root)
text.pack()
text.bind('<KeyRelease>', highlight_xml_syntax)

root.mainloop()

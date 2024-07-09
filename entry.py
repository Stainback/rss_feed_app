from html.parser import HTMLParser


def split_text_on_lines(text: str | list, length: int) -> str:
    words = text.split(" ") if isinstance(text, str) else text
    if len(words) <= length:
        return text if isinstance(text, str) else " ".join(words)
    else:
        return " ".join(words[:length]) + "\n" + split_text_on_lines(words[length:], length)


class EntryParser(HTMLParser):
    def __init__(self, data):
        HTMLParser.__init__(self)

        self.title = data.title
        self.description = ""
        self.link = data.link

        self.feed(data.description)

    def handle_data(self, data):
        self.description += data.strip("\n")

    @property
    def section(self):
        return split_text_on_lines(self.description.split(" ")[:60], 15)

from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    content = ""
    count = 0

    def handle_data(self, data):
        if self.count == 0:
            self.content = data + "..."
            self.count += 1
import html2text

def html_to_markdown(html: str) -> str:
    handler = html2text.HTML2Text()
    handler.ignore_links = True
    handler.ignore_images = True
    handler.ignore_emphasis = True
    handler.body_width = 0  # Don't wrap lines
    return handler.handle(html)
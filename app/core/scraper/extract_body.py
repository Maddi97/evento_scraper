from bs4 import BeautifulSoup

def extract_relevant_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    if not body:
        return ""

    for tag in body.find_all(['script', 'style', 'noscript']):
        tag.decompose()

    for tag in body.find_all():
        if tag.attrs is None:
            continue
        if tag.has_attr('hidden') or tag.has_attr('aria-hidden') or 'display: none' in tag.get('style', ''):
            tag.decompose()

    keywords = ['nav', 'footer', 'modal', 'offcanvas', 'sidebar', 'navigation', 'navbar', 'menu']
    for tag in body.find_all():
        if tag.attrs is None:
            continue

        if tag.name not in ['img', 'br', 'input'] and not tag.get_text(strip=True) and not tag.find('img'):
            tag.decompose()

    return str(body)



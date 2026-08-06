from django import template

register = template.Library()

@register.filter
def first_word(value):
    """Returns the first word of a string."""
    if not value:
        return value
    return value.split()[0]

@register.filter
def youtube_embed_url(url):
    """Converts standard YouTube watch, share, or shorts URLs to a clean embed URL."""
    import re
    if not url:
        return ""
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    return url

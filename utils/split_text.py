def split_text(text: str, max_len: int = 4000) -> list[str]:
    text = text or ""
    parts = []
    while len(text) > max_len:
        cut = text.rfind("\n", 0, max_len)
        if cut == -1 or cut < max_len * 0.6:
            cut = max_len
        parts.append(text[:cut].strip())
        text = text[cut:].lstrip()
    if text.strip():
        parts.append(text.strip())
    return parts
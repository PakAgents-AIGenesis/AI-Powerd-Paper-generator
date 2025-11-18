def split_text_to_chunks(text, max_tokens=512):
    """
    Split text into chunks by paragraphs and token limits.
    """
    # Split text by paragraph
    paragraphs = text.split("\n\n")
    chunks = []

    for para in paragraphs:
        words = para.split()
        # Split paragraph into token-limited chunks
        for i in range(0, len(words), max_tokens):
            chunk = " ".join(words[i:i+max_tokens])
            chunks.append(chunk)

    return chunks

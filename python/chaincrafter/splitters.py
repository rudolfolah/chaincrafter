def split_processed_content(content, char_limit=4000):
    chunks = []
    current_chunk = []
    accumulated_length = 0

    for item in content:
        text_length = len(item['text'])

        if accumulated_length + text_length > char_limit:
            chunks.append(current_chunk)
            current_chunk = []
            accumulated_length = 0

        current_chunk.append(item['text'])
        accumulated_length += text_length

    # Handle any remaining content
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

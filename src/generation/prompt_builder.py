from src.config.settings import MAX_CONTEXT_CHARS


def build_prompt(query: str, docs: list[dict]) -> str:
    context_blocks = []
    for doc in docs:
        chapter = doc.get("chapter", "")
        lesson = doc.get("lesson", "")
        text = doc.get("text", "")
        if len(text) > MAX_CONTEXT_CHARS:
            text = text[:MAX_CONTEXT_CHARS].rstrip() + "\n...\n"
        context_blocks.append(
            """
مواد:
باب: {chapter}
سبق: {lesson}
متن:
{text}
""".strip().format(
                chapter=chapter,
                lesson=lesson,
                text=text,
            )
        )

    context = "\n\n".join(context_blocks)
    return (
        "آپ اسلامیات کے ماہر استاد ہیں۔ درج ذیل مواد کو استعمال کرتے ہوئے سوال کا جواب دیں۔\n\n"
        f"{context}\n\n"
        f"سوال: {query}\n"
        "براہِ کرم مکمل اور درست جواب دیں، صرف اردو میں جواب دیں۔"
    )

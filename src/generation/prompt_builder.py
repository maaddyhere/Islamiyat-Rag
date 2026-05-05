from typing import Iterable


def build_prompt(query: str, docs: list[dict]) -> str:
    context_blocks = []
    for idx, doc in enumerate(docs, start=1):
        chapter = doc.get("chapter", "")
        lesson = doc.get("lesson", "")
        context_blocks.append(
            """
تدریسی مواد:
Chapter: {chapter}
Lesson: {lesson}
Text: {text}
""".strip().format(
                chapter=chapter,
                lesson=lesson,
                text=doc.get("text", ""),
            )
        )

    context = "\n\n".join(context_blocks)
    return (
        "آپ ایک اسلامیات کے ماہر استاد ہیں۔ درج ذیل مواد کو استعمال کرتے ہوئے سوال کا جواب دیں۔\n\n"
        f"{context}\n\n"
        f"سوال: {query}\n"
        "براہِ کرم مکمل اور درست جواب دیں، صرف اردو میں جواب دیں۔"
    )

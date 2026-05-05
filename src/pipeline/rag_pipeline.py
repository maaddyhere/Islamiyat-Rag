from src.config.settings import GROQ_API_KEY
from src.generation.llm_client import generate_answer
from src.generation.prompt_builder import build_prompt
from src.retrieval.retriever import search


class RAGPipeline:
    def __init__(self) -> None:
        self.use_llm = bool(GROQ_API_KEY)

    def run(self, query: str) -> None:
        results = search(query)
        if not results:
            print("کوئی نتیجہ نہیں ملا۔")
            return

        if self.use_llm:
            prompt = build_prompt(query, results)
            answer = generate_answer(prompt)
            print(answer)
            return

        print("GROQ_API_KEY نہیں ملا؛ تلاش شدہ passages دکھا رہا ہوں۔\n")
        for idx, doc in enumerate(results, start=1):
            print(f"---- نتیجہ {idx} (score={doc['score']:.4f}) ----")
            print(f"Chapter: {doc.get('chapter', '')}")
            print(f"Lesson: {doc.get('lesson', '')}")
            print(doc.get("text", ""))
            print()

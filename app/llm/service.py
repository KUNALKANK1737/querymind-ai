from app.llm.ollama import OllamaClient
from app.llm.prompt import build_sql_generation_prompt
from app.schema.models import DatabaseSchema


def generate_sql(
    question: str,
    schema: DatabaseSchema,
    client: OllamaClient,
) -> str:
    prompt = build_sql_generation_prompt(
        question=question,
        schema=schema,
    )

    return client.generate(prompt)
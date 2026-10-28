from app.llm.ollama import OllamaClient
from app.llm.prompt import (
    build_sql_correction_prompt,
    build_sql_generation_prompt,
)
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

def correct_sql(
    question: str,
    failed_sql: str,
    error: str,
    schema: DatabaseSchema,
    client: OllamaClient,
) -> str:
    prompt = build_sql_correction_prompt(
        question=question,
        failed_sql=failed_sql,
        error=error,
        schema=schema,
    )

    return client.generate(prompt)
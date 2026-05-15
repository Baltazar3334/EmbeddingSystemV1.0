"""
LLM worker reranking.
"""

from llm.llm_client import generate


# RERANK WORKERS ==========================================
def rerank_workers(summary, workers):
    workers_text = ""

    for i, worker in enumerate(workers):
        workers_text += f"""
Worker {i + 1}:
Name: {worker['name']}

Keywords:
{", ".join(worker['keywords'])}

Embedding score:
{worker['score']}

"""

    prompt = f"""
You are an expert research coordinator.

Below is a research contract summary and a list of candidate researchers.

Your task:
- analyze relevance
- evaluate expertise fit
- rerank the workers from best to worst

Focus on:
- domain expertise
- technical fit
- scientific relevance
- research relevance

CONTRACT SUMMARY:
{summary}

CANDIDATE WORKERS:
{workers_text}

Return:
- ordered ranking (return only the names of the ranked workers)
"""

    result = generate(prompt)

    return result
"""
LLM worker evaluation.
"""

import json

from llm.llm_client import generate


# EVALUATE WORKER =========================================
def evaluate_worker(

    contract_text,

    worker
):

    prompt = prompt = f"""
You are an expert evaluator of research teams.

Your task is to evaluate ONE researcher
for ONE research contract.

Evaluate:
- expertise relevance
- domain fit
- technical fit
- scientific relevance
- medical relevance

SCORING RULES 0-100:
0-10 = poor fit
30-40 = weak fit
50-60 = moderate fit
70-80 = strong fit
90-100 = excellent fit

IMPORTANT RULES:
- Return ONLY valid JSON
- Do not add explanations outside JSON
- Do not use markdown
- Do not add extra text
- Keep reason under 20 words

RETURN FORMAT:
{{
    "llm_score": number,
    "reason": "short explanation"
}}

CONTRACT:
{contract_text[:2000]}

RESEARCHER:

Name:
{worker['name']}

Keywords:
{", ".join(worker['keywords'][:5])}

bio:
{worker.get('bio', '')[:1000]}

Embedding similarity:
{worker['semantic_score']}
"""

    response = generate(prompt)

    try:

        result = json.loads(response)

        return result

    except Exception:

        return {
            "llm_score": 0,
            "reason": "LLM parsing failed"
        }
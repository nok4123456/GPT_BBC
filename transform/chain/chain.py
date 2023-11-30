from dotenv import load_dotenv

from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub


def init_llm(repo_id: str, model_kwargs: dict = None):
    return HuggingFaceHub(repo_id=repo_id, model_kwargs=model_kwargs)


def init_prompt_template(prompt_template: str):
    return ChatPromptTemplate.from_template(prompt_template)


def init_chain():
    REPO_ID = "facebook/bart-large-cnn"
    MODEL_KWARGS = {"temperature": 0.5, "max_length": 150}
    PROMPT_TEMPLATE = """Write a concise and easy english summary of the following. Using around 100 words: "{text}" CONCISE SUMMARY:"""

    llm = init_llm(REPO_ID, MODEL_KWARGS)
    prompt = init_prompt_template(PROMPT_TEMPLATE)
    return prompt | llm


def invoke_chain(chain, docs: str):
    return chain.invoke({"text": docs})

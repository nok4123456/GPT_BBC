# %%
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from langchain.llms import HuggingFaceEndpoint
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.prompts import ChatPromptTemplate


def init_llm(repo_id: str, model_kwargs: dict = None):
    return HuggingFaceHub(repo_id=repo_id, model_kwargs=model_kwargs)


def init_prompt_template(prompt_template: str):
    return ChatPromptTemplate.from_template(prompt_template)


def init_cnn_chain():
    REPO_ID = "facebook/bart-large-cnn"
    MODEL_KWARGS = {"temperature": 0.5, "max_length": 150}
    PROMPT_TEMPLATE = """Write a concise and easy english summary of the following. Using around 100 words: "{text}" CONCISE SUMMARY:"""

    llm = init_llm(REPO_ID, MODEL_KWARGS)
    prompt = init_prompt_template(PROMPT_TEMPLATE)
    return prompt | llm


def init_tw_llm_inference_endpoint():
    ENDPOINT_URL = "https://wsruuij88x0cp23u.us-east-1.aws.endpoints.huggingface.cloud"
    hf = HuggingFaceEndpoint(endpoint_url=ENDPOINT_URL, task="text2text-generation")
    return hf


def init_tw_chain():
    PROMPT_TEMPLATE = """翻譯成五個重點:"{text}"""

    llm = init_tw_llm_inference_endpoint()
    prompt = init_prompt_template(PROMPT_TEMPLATE)
    return prompt | llm


def invoke_chain(chain, docs: str):
    return chain.invoke({"text": docs})


# %%

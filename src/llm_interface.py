"""LLM interface for calling models – compatible with OpenAI, Ollama and other LLMs."""
import json
import logging

import litellm

from consts import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMCaller:
    """Interface for LLM interaction."""

    def __init__(
            self,
            model_name: str = LLM_MODEL_NAME,
            llm_api_key: str = LLM_API_KEY,
            llm_base_url: str = LLM_BASE_URL,
            prompt: str | None = None):
        """
        Parameters
        ----------
        model_name : str, optional
            Usually provider/model_name, not for openai though.
            E.g. "gpt-4o",
            "ollama/qwq:32b-preview-q4_K_M",
            "mistral/mistral-tiny", by default LLM_MODEL_NAME
        llm_api_key : str, optional
            LLM Secret, necessary for openai, unnecessary for ollama,
            by default LLM_API_KEY
        llm_base_url : str, optional
            Necessary if using proxy url for openai,
            if running locally "http://localhost:11436", by default LLM_BASE_URL
        prompt : str | None, optional
            Constant prompt for queries, by default None
        """
        self.model_name = model_name
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url
        self.prompt = prompt

    def call_model(self,
                   call_params: dict[str, str] | None = None,
                   prompt: str | None = None,
                   **kwargs) -> litellm.ModelResponse:
        """
        Parameters
        ----------
        call_params : dict[str, str] | None, optional
            Parameters to format prompt variables,
            if empty then set to {}, by default None
        prompt : str | None, optional
            Prompt to send, if empty then set to self.prompt, by default None

        Returns
        -------
        litellm.ModelResponse
        """
        if prompt is None:
            prompt = self.prompt
        if call_params is None:
            call_params = {}
        messages = [{"role": "user",
                    "content": prompt.format(**call_params)}]
        response = litellm.completion(
            model=self.model_name,
            messages=messages,
            api_key=self.llm_api_key,
            api_base=self.llm_base_url,
            **kwargs
        )
        logger.info(
            "Got response for call_params %s (300 symbols):\n %s...",
            str(call_params), response['choices'][0]['message']['content'][:300])
        logger.info("Total cost %s",  litellm.completion_cost(response))
        return response

    @staticmethod
    def get_response_content(response: litellm.ModelResponse) -> str | dict:
        try:
            result = response['choices'][0]['message']['content']
            return json.loads(result)
        except json.JSONDecodeError:
            return result

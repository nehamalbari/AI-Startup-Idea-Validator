import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
from pydantic import PrivateAttr


load_dotenv()


class GeminiFallbackLLM(ChatGoogleGenerativeAI):

    _fallback_models: list = PrivateAttr(default_factory=list)
    _current_key_index: int = PrivateAttr(default=0)

    def set_fallback_models(self, models):
        self._fallback_models = models

    def _generate(
        self,
        messages: list[BaseMessage],
        stop=None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs
    ) -> ChatResult:

        models = [self] + self._fallback_models

        for index, model in enumerate(models):

            try:
                print(
                    f"\n[Gemini Router] Trying API Key {index + 1}"
                )

                if model is self:
                    result = super()._generate(
                        messages,
                        stop=stop,
                        run_manager=run_manager,
                        **kwargs
                    )
                else:
                    result = model._generate(
                        messages,
                        stop=stop,
                        run_manager=run_manager,
                        **kwargs
                    )

                print(
                    f"[Gemini Router] API Key {index + 1} succeeded"
                )

                return result

            except Exception as e:

                error_text = str(e)

                print(
                    f"[Gemini Router] API Key {index + 1} failed"
                )

                if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                    print(
                        f"[Gemini Router] Quota exhausted for "
                        f"API Key {index + 1}"
                    )

                    if index < len(models) - 1:
                        print(
                            f"[Gemini Router] "
                            f"Switching to API Key {index + 2}"
                        )
                        continue

                raise

        raise RuntimeError(
            "All configured Gemini API keys have been exhausted."
        )


def create_gemini_model(api_key):

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key
    )


# --------------------------------------------------
# Load API keys
# --------------------------------------------------

api_keys = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
    os.getenv("GEMINI_API_KEY_4"),
    os.getenv("GEMINI_API_KEY_5"),
]

api_keys = [
    key for key in api_keys
    if key
]

if not api_keys:
    raise ValueError(
        "No Gemini API keys found in environment variables."
    )


print(
    f"[Gemini Router] Loaded {len(api_keys)} API keys"
)


# --------------------------------------------------
# Create primary model
# --------------------------------------------------

llm = GeminiFallbackLLM(
    model="gemini-3.6-flash",
    google_api_key=api_keys[0]
)


# --------------------------------------------------
# Create fallback models
# --------------------------------------------------

fallback_models = [
    create_gemini_model(key)
    for key in api_keys[1:]
]


llm.set_fallback_models(fallback_models)
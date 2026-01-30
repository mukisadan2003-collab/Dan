import os
import requests
import logging
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class OllamaClient:
    def __init__(self, base_url=None, model=None, timeout=30, max_retries=3, backoff_factor=0.3):
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "local-llm")
        self.timeout = timeout

        self.session = requests.Session()
        retries = Retry(total=max_retries,
                        backoff_factor=backoff_factor,
                        status_forcelist=[429, 500, 502, 503, 504],
                        allowed_methods=["POST"])
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _try_endpoints(self, payload, candidates):
        headers = {"Content-Type": "application/json"}
        for path in candidates:
            url = urljoin(self.base_url, path)
            try:
                logger.debug("Calling Ollama: %s", url)
                r = self.session.post(url, json=payload, headers=headers, timeout=self.timeout)
                logger.debug("Response status: %s", r.status_code)
                if r.status_code == 200:
                    try:
                        data = r.json()
                        # Common patterns
                        if isinstance(data, dict):
                            if "choices" in data and data["choices"]:
                                ch = data["choices"][0]
                                return ch.get("text") or ch.get("message") or str(ch)
                            if "text" in data:
                                return data["text"]
                            if "result" in data:
                                return data["result"]
                        return r.text
                    except ValueError:
                        return r.text
            except requests.RequestException as e:
                logger.debug("Endpoint %s failed: %s", url, e)
                continue
        return None

    def generate(self, prompt, max_tokens=512, temperature=0.7):
        payload = {"model": self.model, "prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
        candidates = [
            "/api/generate",
            "/api/completions",
            f"/models/{self.model}/generate",
            f"/{self.model}",
            "/completions",
            "/generate",
        ]
        result = self._try_endpoints(payload, candidates)
        if result is not None:
            return result
        raise RuntimeError("Failed to contact Ollama at configured endpoints. Check base_url and service status.")

_default_client = None

def get_client():
    global _default_client
    if _default_client is None:
        _default_client = OllamaClient()
    return _default_client

"""
SkillBridge AI — spaCy & NLP Dependency Helper

Wraps spaCy initialization inside a dynamic loader with try-except fallback 
to ensure the FastAPI server starts cleanly even if spaCy fails to install or load.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger("skillbridge.ai.nlp")

# Cache NLP pipeline instance
_nlp = None

def get_spacy_nlp() -> Any:
    """
    Get or load the spaCy 'en_core_web_sm' pipeline.
    Gracefully falls back to None if spaCy is missing or fails to load.
    """
    global _nlp
    if _nlp is not None:
        return _nlp

    try:
        import spacy
        try:
            _nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy 'en_core_web_sm' pipeline loaded successfully.")
        except OSError:
            logger.warning("spaCy 'en_core_web_sm' model not found. Attempting to download...")
            try:
                from spacy.cli import download
                download("en_core_web_sm")
                _nlp = spacy.load("en_core_web_sm")
                logger.info("spaCy 'en_core_web_sm' downloaded and loaded successfully.")
            except Exception as download_err:
                logger.error("Failed to download spaCy en_core_web_sm model: %s", download_err)
                _nlp = False
    except ImportError:
        logger.warning("spaCy package is not installed. Running in spaCy-free fallback mode.")
        _nlp = False
    except Exception as err:
        logger.error("Unexpected error during spaCy load: %s", err)
        _nlp = False

    return _nlp

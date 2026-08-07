#!/usr/bin/env python3
"""
VANGUARD Pro - Main Entry Point
Self-Evolving Cognitive Agent for Devin.ai
"""

import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent))

from api.server import app  # noqa: E402
from utils.logger import logger, setup_logging  # noqa: E402


def main():
    """تشغيل الخادم الرئيسي"""
    setup_logging()

    logger.info("VANGUARD Pro - Starting up...")
    logger.info(f"Working directory: {Path.cwd()}")

    port = int(os.getenv("VANGUARD_API_PORT", "8000"))
    host = os.getenv("VANGUARD_API_HOST", "0.0.0.0")

    logger.info(f"Starting API server on http://{host}:{port}")
    logger.info("VANGUARD Agent is ready!")

    uvicorn.run(app, host=host, port=port, log_level="info", access_log=True)


if __name__ == "__main__":
    main()

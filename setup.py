from setuptools import setup, find_packages

setup(
    name="vanguard-devin-agent",
    version="1.0.0",
    description="VANGUARD Pro - Self-Evolving Cognitive Agent for Devin.ai",
    author="VANGUARD Team",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "pydantic-settings",
        "torch",
        "numpy",
        "pinecone-client",
        "google-generativeai",
        "loguru",
        "psutil",
        "python-dotenv",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "vanguard=main:main",
        ],
    },
)

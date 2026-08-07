from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent.orchestrator import VanguardOrchestrator
from utils.logger import logger


class AnalyzeRequest(BaseModel):
    project_path: str
    code_content: Optional[str] = None


class BuildRequest(BaseModel):
    project_path: str
    target: str


class DiagnoseRequest(BaseModel):
    error_message: str
    project_path: str
    code_context: Optional[str] = None


class FeedbackRequest(BaseModel):
    features: Dict[str, float]
    context: Dict[str, float]
    correct_path: int


app = FastAPI(
    title="VANGUARD Pro Agent",
    description="Self-Evolving Cognitive Agent for Devin.ai",
    version=VanguardOrchestrator.VERSION,
)

orchestrator = VanguardOrchestrator()


@app.on_event("startup")
async def startup_event():
    logger.info("VANGUARD Agent starting up...")
    logger.info(f"Stats: {orchestrator.stats}")


@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_project(req: AnalyzeRequest):
    """تحليل مشروع برمجي"""
    try:
        result = orchestrator.analyze(req.project_path, req.code_content)
    except Exception as exc:
        logger.error(f"Analysis failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    logger.info(f"Analysis complete: {req.project_path}")
    return {"status": "success", "data": result}


@app.post("/build", response_model=Dict[str, Any])
async def build_project(req: BuildRequest):
    """بناء المشروع مع تصحيح ذاتي"""
    try:
        result = orchestrator.build(req.project_path, req.target)
    except Exception as exc:
        logger.error(f"Build failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    logger.info(f"Build result: {result.get('status')} - {req.project_path}")
    return result


@app.post("/diagnose", response_model=Dict[str, Any])
async def diagnose_error(req: DiagnoseRequest):
    """تشخيص خطأ واقتراح حلول"""
    try:
        solutions = orchestrator.diagnose(
            req.error_message, req.project_path, req.code_context
        )
    except Exception as exc:
        logger.error(f"Diagnosis failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    logger.info(f"Diagnosis complete: {len(solutions)} solutions found")
    return {"status": "success", "solutions": solutions}


@app.post("/feedback", response_model=Dict[str, Any])
async def provide_feedback(req: FeedbackRequest):
    """تقديم تغذية راجعة للتعلم"""
    try:
        loss = orchestrator.learn_from_feedback(
            req.features, req.context, req.correct_path
        )
    except Exception as exc:
        logger.error(f"Feedback failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    logger.info(f"Training loss: {loss:.4f}")
    return {"status": "success", "loss": loss}


@app.get("/stats", response_model=Dict[str, Any])
async def get_stats():
    """الحصول على إحصائيات النظام"""
    return {"status": "success", "stats": orchestrator.stats}


@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """فحص صحة النظام"""
    return orchestrator.health_check()


@app.get("/memory/{query}", response_model=Dict[str, Any])
async def search_memory(query: str, top_k: int = 5):
    """البحث في الذاكرة عن حلول لخطأ معين"""
    try:
        results = orchestrator.memory.search_by_error(query, top_k)
    except Exception as exc:
        logger.error(f"Memory search failed: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    return {"status": "success", "results": results}

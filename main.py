from fastapi import FastAPI, HTTPException
from typing import List, Union
from src.pipeline import run_pipeline

app = FastAPI()


@app.post("/validate")
def validate(events: Union[dict, List[dict]]):

    try:
        # ✅ STEP 1: Normalize input (single → list)
        if isinstance(events, dict):
            events = [events]

        # ✅ STEP 2: Run pipeline
        results = run_pipeline(events)

        if not results:
            raise HTTPException(
                status_code=400,
                detail="No output generated from pipeline"
            )

        # ✅ STEP 3: Check if ALL signals rejected
        all_rejected = all(
            ("validation" in r and r["validation"]["status"] == "REJECT")
            or "error" in r
            for r in results
        )

        if all_rejected:
            raise HTTPException(
                status_code=400,
                detail="All signals rejected. Pipeline stopped."
            )

        # ✅ STEP 4: Return full structured output
        return {
            "results": results
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
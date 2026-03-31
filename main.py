from fastapi import FastAPI, HTTPException
from src.pipeline import run_pipeline

app = FastAPI()


@app.post("/validate")
def validate(event: dict):
    try:
        # 🚨 STEP 1: Run pipeline
        result = run_pipeline([event])

        # 🚨 STEP 2: Safety check
        if not result:
            raise HTTPException(
                status_code=400,
                detail="Validation failed. No output generated."
            )

        output = result[0]

        # 🚨 STEP 3: Handle REJECT
        if output.get("status") == "REJECT":
            raise HTTPException(
                status_code=400,
                detail="Validation failed. Pipeline stopped."
            )

        # ✅ STEP 4: ALLOW / FLAG → return success
        return output

    except HTTPException:
        # Already handled → just re-raise
        raise

    except Exception as e:
        # 🚨 Catch ALL unexpected errors (prevent 500)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
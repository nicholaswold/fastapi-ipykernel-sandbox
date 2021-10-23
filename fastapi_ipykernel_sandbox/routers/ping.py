from fastapi import APIRouter, status

router = APIRouter()


@router.get("/ping", status_code=status.HTTP_204_NO_CONTENT)
async def ping():
    pass

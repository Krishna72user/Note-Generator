from fastapi import APIRouter,Response,Cookie,HTTPException,Depends
from app.services.generator import generate_notes,summarize
from app.schemas.prompt import Prompt_model
from app.utils.jwt_util import verify_token
from app.db.database import get_connection

router = APIRouter(tags=["Notes"],prefix='/notes')

@router.post('/generate')
def generate(prompt:Prompt_model,access_token: str = Cookie(None),conn = Depends(get_connection)):
    payload = verify_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    email= payload['email']

    pdf,response = generate_notes(prompt.prompt,prompt.title)
    summary = summarize(response)

    with conn.cursor() as cursor:
        query = """
        INSERT INTO notes
        (title,summary,user_email)
        VALUES
        (%s,%s,%s)
        """
        cursor.execute(query,(prompt.title,summary,email))

    conn.commit()
    conn.close()
    return Response(
        content=pdf,
        media_type="application/pdf"
    )

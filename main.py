from decouple import config
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import openai

from database import SessionLocal, init_db, TextSummary


openai.api_key = config('OPENAI_API_KEY')

app = FastAPI()


init_db()


def get_db():
    """
    Dependency that provides a database session to route functions.

    Yields:
        Session: SQLAlchemy database session.

    Closes the session after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TextRequest(BaseModel):
    """
    Data model for the text input used in the `/process_text/` endpoint.

    Attributes:
        text (str): The input text to be processed.
    """
    text: str

def generate_summary(text):
    """
    Generates a summary of the provided text using OpenAI's GPT-4 model.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The generated summary of the input text.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ]
    )
    return response.choices[0].message['content']

def extract_entities(text):
    """
    Extracts named entities (such as people, organizations, and locations) from the provided text
    using OpenAI's GPT-4 model.

    Args:
        text (str): The text from which to extract entities.

    Returns:
        str: The extracted named entities.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Extract named entities (such as people, organizations, and locations) from the following text:\n\n{text}"}
        ]
    )
    return response.choices[0].message['content']

@app.post("/process_text/")
def process_text(request: TextRequest, db: Session = Depends(get_db)):
    """
    Endpoint to process input text by generating a summary and extracting entities.

    Args:
        request (TextRequest): The input text provided in the request body.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the summary, extracted entities, and the database ID.
    """
    summary = generate_summary(request.text)
    entities = extract_entities(request.text)

    # Save to the database
    db_summary = TextSummary(original_text=request.text, summary=summary, entities=entities)
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)

    return {"summary": summary, "entities": entities, "id": db_summary.id}

@app.get("/summaries/{summary_id}")
def get_summary(summary_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a stored summary and its entities by the given summary ID.

    Args:
        summary_id (int): The ID of the summary to retrieve.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        TextSummary: The retrieved summary and entities.

    Raises:
        HTTPException: If the summary with the given ID is not found.
    """
    db_summary = db.query(TextSummary).filter(TextSummary.id == summary_id).first()
    if db_summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    return db_summary

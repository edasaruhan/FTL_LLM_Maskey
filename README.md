
FastAPI Application for Text Processing using OpenAI's GPT-4

This application provides endpoints to process text by generating a summary and extracting named entities.
It utilizes OpenAI's GPT-4 model for natural language processing tasks. The results are stored in a SQLite 
database using SQLAlchemy as the ORM.

Modules and Libraries:
- `decouple`: Used for loading environment variables, specifically the OpenAI API key.
- `FastAPI`: The web framework used to build the API.
- `SQLAlchemy`: ORM used to interact with the SQLite database.
- `openai`: Python library to interact with OpenAI's API.

Environment Variables:
- `OPENAI_API_KEY`: The API key for accessing OpenAI's services.

Database Models:
- `TextSummary`: SQLAlchemy model to store the original text, its summary, and extracted entities.

Routes:
- POST `/process_text/`: Accepts text input, generates a summary and extracts named entities, then stores
  the results in the database.
- GET `/summaries/{summary_id}`: Retrieves a stored summary and its entities by the given summary ID.


Usage:
1. Set the `OPENAI_API_KEY` environment variable.
2. Install all libraries by `pip install -r requirements.txt`
3. Start the FastAPI server using `uvicorn main:app --reload`.
4. Use the `/process_text/` endpoint to process text and store results.
5. Retrieve stored summaries and entities using the `/summaries/{summary_id}` endpoint.

   

![Screenshot 2024-08-11 215026](https://github.com/user-attachments/assets/e4cd527d-4342-45fc-b56f-d35e9493e1c9)


![Screenshot 2024-08-11 220147](https://github.com/user-attachments/assets/c672f31e-6dc9-4c2d-8a66-20a0b9e710a7)






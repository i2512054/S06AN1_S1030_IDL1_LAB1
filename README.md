```bash
python -m venv .lab01
source .lab01/bin/activate        # en Windows: .lab01\Scripts\activate
 
# pip install fastapi uvicorn pydantic openai python-dotenv google-genai
pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
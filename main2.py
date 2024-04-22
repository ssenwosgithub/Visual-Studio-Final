# Import necessary libraries
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from textblob import TextBlob
from typing import Optional

# Define the Text model
class Text(BaseModel):
    content: str
    sentiment: Optional[float]

# Define the sentiment analysis function
def analyze_sentiment(text: str):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return Text(content=text, sentiment=sentiment)

# Create the FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define the route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, text: str):
    sentiment = analyze_sentiment(text)
    if not sentiment:
        raise HTTPException(status_code=400, detail="Invalid text.")
    return templates.TemplateResponse("index.html", {"request": request, "text": text, "sentiment": sentiment.sentiment})

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

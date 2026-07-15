from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import logging

from AI_Assistant.database import SessionLocal, engine
from AI_Assistant.model import Base, User
from AI_Assistant.Ai_agent import State_graph
from openai import RateLimitError


# ------------------------
# INIT
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


# ------------------------
# CONFIG
# ------------------------
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ------------------------
# DATABASE
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# JWT
# ------------------------
def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ------------------------
# SCHEMAS
# ------------------------
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

class SignUpRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str


# ------------------------
# ROOT
# ------------------------
@app.get("/")
async def root():
    return {"message": "API running 🚀"}


# ------------------------
# SIGNUP (DB)
# ------------------------
@app.post("/signup")
async def sign_up(request: SignUpRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.username == request.username).first()

    if existing:
        raise HTTPException(400, "User already exists")

    hashed_password = pwd_context.hash(request.password)

    new_user = User(
        username=request.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"msg": "Signup successful"}


# ------------------------
# LOGIN (DB + JWT)
# ------------------------
@app.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == request.username).first()

    if not user or not pwd_context.verify(request.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(user.username)

    return {"access_token": token}


# ------------------------
# CHAT MEMORY (per user)
# ------------------------
user_states = {}


# ------------------------
# CHAT (Protected)
# ------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: str = Depends(get_current_user)
):

    # Initialize user state
    if user not in user_states:
        user_states[user] = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are Janet, a cheerful and witty assistant..."
                }
            ]
        }

    state = user_states[user]

    # Add user message
    state["messages"].append({
        "role": "user",
        "content": request.query
    })

    logging.info(f"{user}: {request.query}")

    try:
        state = State_graph().invoke(state)
        user_states[user] = state
    except RateLimitError:
        return ChatResponse(
            response="⚠️ Server busy, try again later"
        )

    last_response = state["messages"][-1]["content"]

    return ChatResponse(response=last_response)
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from jose import jwt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Database setup
DATABASE_URL = "mysql+pymysql://lab:pR0g_fUn_lAb@localhost/project-chatbot"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT setup
SECRET_KEY = "pR0g_fUn_lAb"
ALGORITHM = "HS256"

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLAlchemy Model for the "users" table
class User(Base):
    __tablename__ = "users"

    idusers = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))

Base.metadata.create_all(bind=engine)

# Pydantic models for request validation
class RegisterUser(BaseModel):
    username: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility function to hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Utility function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Utility function to create JWT token
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Registration endpoint
@app.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and store it in the database
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}

# Login endpoint
@app.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    # Retrieve the user by username
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Verify the provided password against the hashed password in the database
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate a JWT token for the user
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Interactive Chatbot Project

## Overview
This project is an interactive chatbot that uses OpenAI's API for natural language processing and supports both text and voice inputs.

## Features
- Responds to user input using OpenAI's GPT model.
- Supports both text and voice inputs with fallback options.
- Optional integration with 2D/3D characters.

## API Key
The API key is available in your Telegram (tele).

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Create a virtual environment and activate it**:
   ```bash
   Windows: venv\Scripts\activate

3. **Pip Install Packages**:
   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql passlib python-jose bcrypt passlib

3. **Install Node JS (for frontend to work)**:
   ```bash
   https://nodejs.org/en/download/package-manager/current

4. **On VS Code install these extendsions**:
   ```bash
   ESLint
   Prettier - Code Formatter

---

## To start Frontend
1. **In terminal**:
   ```bash
   npm start
   
## To start backend
1. **In terminal**:
   ```bash
   uvicorn mainapp:app --reload

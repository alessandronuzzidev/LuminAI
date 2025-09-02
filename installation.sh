# Manualmente instalar Ollama y Python3.12 o superior

python3 -m venv venv
source venv/bin/activate 
pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --windowed --onefile --name LuminAI main.py
./dist/LuminAI

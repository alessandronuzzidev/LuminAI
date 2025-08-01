mkdir tfm
cd tfm
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install openai python-dotenv requests
pip install azure-identity
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login --use-device-code
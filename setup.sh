# Install python dependencies
sudo python3 -m pip install selenium twitter

# Install Chrome
sudo apt-get -y install google-chrome-stable

# Download Chromedriver
OS_PREFFIX=""
if [[ "${OSTYPE}" == "msys" ]]; then
    OS_PREFFIX="win32"
elif [[ "${OSTYPE}" == "linux-gnu" ]]; then
    OS_PREFFIX="linux64"
elif [[ "${OSTYPE}" == "darwin*" ]]; then
    OS_PREFFIX="mac64"
else
    echo "Unknown system, download Chromedriver manually."
    exit 1
fi

wget "https://chromedriver.storage.googleapis.com/73.0.3683.20/chromedriver_${OS_PREFFIX}.zip" --output-document=chromedriver.zip
sudo apt-get -y install unzip
unzip chromedriver.zip
chmod a+x chromedriver
rm chromedriver.zip

mkdir files
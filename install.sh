virtualenv -p python3 Kavvas_env
source Kavvas_env/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
git clone  https://github.com/nemurici/python3-wappalyzer.git ./Kavvas_env/lib/python3.6/site-packages/Wappalyzer/
deactivate

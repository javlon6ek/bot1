echo "3.11" > .python-version
git add .python-version
git commit -m "Added Python version"
git push origin main
pip install aiohttp==3.8.5


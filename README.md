# List-YouTube
Automatically create and post YouTube playlists and videos

- py to exe
```
pyinstaller .\main.py --hidden-import=pkg_resources.py2_warn --onefile --noconsole --add-binary ".\webdrivers\chromedriver.exe;.\webdrivers" --version-file ".\CI\version.py"
```
- hide chromeDriver console in python
```
https://stackoverflow.com/questions/33983860/hide-chromedriver-console-in-python
```

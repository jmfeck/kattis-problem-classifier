@echo off
echo Starting the script...

call activate kattis-problems-classifier

cd scripts
python kattis-scrapper.py

echo Script completed.
pause

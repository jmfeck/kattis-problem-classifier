@echo off
echo Starting the script...

call activate openai-test

cd scripts
python kattis-problem-classifier.py

echo Script completed.
pause

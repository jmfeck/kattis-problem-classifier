@echo off
echo Starting the script...

call activate openai-test

cd scripts
python kattis_problem_classifier.py

echo Script completed.
pause

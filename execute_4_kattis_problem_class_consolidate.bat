@echo off
echo Starting the script...

call activate kattis-problems-classifier

cd scripts
python kattis_problem_classifier_consolidation.py

echo Script completed.
pause
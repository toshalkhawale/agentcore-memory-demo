@echo off
echo ========================================
echo GitHub Push Script
echo ========================================
echo.
echo When prompted:
echo Username: toshalkhawale
echo Password: [paste your GitHub Personal Access Token here]
echo.
pause

git push -u origin main

echo.
echo ========================================
echo Push complete!
echo ========================================
pause

@echo off

call "%~dp0..\run.bat" --vfs-path "test.zip" --strt-scr-path "tests\script2.txt"  --cmd-promt "write here >>" --log-path "logs\log1.csv"

pause
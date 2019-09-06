# lab monitor #
This project captures student mouse and keyboard events to a AWS APIgateway API with a API key.  
It can run unittest inside AWS Lambda and send back the unit test result to students.  
Run the following command to run the monitor.  
python monitor.py -m "absolute path directory" -a "APIGateway endpoint" -k "Api key"

For Windows, you can create a batch script and in the following folder structure.

\ite3101_introduction_to_programming

\labmonitor

run.bat

You have to create your virtual environment and install all dependencies.

.\labmonitor\venv\Scripts\activate.bat && python.exe labmonitor/monitor.py ^
-m ite3101_introduction_to_programming ^
-a https:/XXXXX.execute-api.us-east-1.amazonaws.com/Prod/ ^
-k APIKey

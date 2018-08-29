# lab monitor #
This project captures student mouse and keyboard events to a AWS APIgateway API with a API key.  
It can run unittest inside AWS Lambda and send back the unit test result to students.  
Run the following command to run the monitor.  
python monitor.py -m <absolute path directory> -a <url> -k <apikey>
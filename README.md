(1) Install python-3.9.6
(2) Install all packages from REQUIREMENTS.txt
(3) Install TA-lib library, can be done via conda.
(4) In the home directory of this project, create a ".env" file and put the following in it and then save it:
        
           API_KEY="1s3SY30ujJ1yNLIX5yhjTX8EEWAeqdW6mR5QhedqDcIIrH69WkbeYmNN8kjxfIAZ"
           API_SECRET="gl1nTytsG3ZqQCsbrkeRC0rwp2rGRA9Ic6eVoQJne0eelFKwTbWHpfEGKkjpmP3d"

(4) Now create a kafka producer topic, with topic-name = 'dogetopic'
(5) Now, start listening from 'dogetopic' in a kafka-consumer-terminal.
(6) Now run the 'main.py' file.(WE WOULD THEN HAVE TO WAIT TILL THE TIME ANY CROSSOVERS HAPPENS FOR ANYTHING TO SHOW UP IN OUTPUT).
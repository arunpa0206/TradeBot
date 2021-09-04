##################################################################################################################################
(0) Create a docker network : 'docker network create advisory', if it doesn;t already exists.

(1) Run the command : 'docker-compose build' 

(3) After the building is complete, run the command : 'docker run -it --network=advisory client' (Running the image)
(4) Now wait till you enter the anaconda prompt, once in, run the command : 'python main.py' 
(5) The code will be running with an initial message : "main.py is running" 

##################################################################################################################################

(#) If the code gives an error: of type 'API-error' then, create a ".env" file and put the following in it the tradebot-code folder and then save it:
        
           API_KEY="1s3SY30ujJ1yNLIX5yhjTX8EEWAeqdW6mR5QhedqDcIIrH69WkbeYmNN8kjxfIAZ"
           API_SECRET="gl1nTytsG3ZqQCsbrkeRC0rwp2rGRA9Ic6eVoQJne0eelFKwTbWHpfEGKkjpmP3d"


## NO OTHER OUTPUT SHOULD COME UP IN THE TERMINAL, EXCEPT THE ONCE MENTIONED.
## Image name made == 'client'
## Network name == 'advisory'
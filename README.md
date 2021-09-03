##################################################################################################################################

(1) Run the command : 'docker-compose up' (Setting up the kafka-server)
(2) Now create a kafka producer topic, with topic-name = DOGEUSDTTOPIC. -->
         A) Open 'localhost:9000', after the docker-compose has fully created the kafka-server (run 'docker ps -q', if 5 new             instances(zookeeper , kafka1 , kafka2 , kafka3 , kafdrop) has been created then everything is running!), in             localhost:9000-UI, locate 'Topics' and click on 'new', then create a new topic "DOGEUSDTTOPIC", with rep-factor=3,                     partitions=3.
(3) Now, in a new terminal, run the command : 'docker build -t client .' (Building the image)
(4) After the building is complete, run the command : 'docker run -it --network=advisory client' (Running the image)
(5) Now wait till you enter the anaconda prompt, once in, run the command : 'python main.py' 
(6) The code will be running with an initial message : "main.py is running" 

##################################################################################################################################

(7) If the code gives an error: of type 'API-error' then, create a ".env" file and put the following in it the tradebot-code folder and then save it:
        
           API_KEY="1s3SY30ujJ1yNLIX5yhjTX8EEWAeqdW6mR5QhedqDcIIrH69WkbeYmNN8kjxfIAZ"
           API_SECRET="gl1nTytsG3ZqQCsbrkeRC0rwp2rGRA9Ic6eVoQJne0eelFKwTbWHpfEGKkjpmP3d"


## NO OTHER OUTPUT SHOULD COME UP IN THE TERMINAL, EXCEPT THE ONCE MENTIONED.
## Image name made == 'client'
## Network name == 'advisory'
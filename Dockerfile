FROM  continuumio/miniconda3

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . $APP_HOME

#---------------- Prepare the envirennment
RUN conda install -c conda-forge ta-lib
RUN pip install -r REQUIREMENTS.txt

SHELL ["conda", "run", "--name", "app", "/bin/bash", "-c"]
CMD ["python", "main.py"]

#ENTRYPOINT ["conda", "run", "--name", "app", "python", "main.py"]
#ENTRYPOINT ["python3"]FROM python:3
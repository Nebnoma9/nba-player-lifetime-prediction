FROM frolvlad/alpine-miniconda3:python3.7

#RUN conda create --name nba-env python=3.8 --yes
#SHELL ["conda", "run", "-n", "nba-env", "/bin/sh", "-c"]

COPY requirements.txt .

RUN pip install -r requirements.txt && rm requirements.txt

EXPOSE 80

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
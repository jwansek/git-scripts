FROM jonashaag/klaus:latest
MAINTAINER Eden Attenborough "eda@e.email"
ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./klaus.css /usr/lib/python3.10/site-packages/klaus/static
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]


FROM alpine:3.16.8
RUN apk add --update \
  python3 \
  py-pip \
  python3-dev \
  gcc \
  make 
RUN pip install --upgrade pip
RUN echo Copying the Mythical Mysfits Flask service into a service directory.
COPY ./service/requirements.txt /MythicalMysfitsService/
WORKDIR /MythicalMysfitsService
RUN echo Installing Python packages listed in requirements.txt
RUN pip install -r ./requirements.txt
COPY ./service /MythicalMysfitsService
RUN echo Starting python and starting the Flask service...
ENTRYPOINT ["python3"]
CMD ["mysfits_like.py"]


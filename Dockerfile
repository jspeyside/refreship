FROM python:3.7-alpine

ENV NS1_API_KEY \
    ZONE \
    DOMAIN_NAME \
    LOG_LEVEL=info

ADD refreship.py /refreship.py
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
CMD /refreship.py
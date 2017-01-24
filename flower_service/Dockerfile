FROM python:3.5

ADD . /opt/flower/

ADD flowerconfig.py  /opt/flower/
ADD run-flower.sh /opt/flower/
RUN chmod +x /opt/flower/run-flower.sh

WORKDIR /opt/flower/

RUN python3 -m pip install -r requirements.txt

#EXPOSE 5555

CMD ["/opt/flower/run-flower.sh"]
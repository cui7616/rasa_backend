######################################################################
#  This Dockerfile is used build your Rasa image                     #
######################################################################

# RASA_IMAGE is passed from docker-compose.yml which is generated
# from ./botfront/docker-compose-template.yml and ./botfront/botfront.yml

FROM rasa/rasa:2.8.29-full

# Change back to root user to install dependencies
USER root

COPY ./run.py /opt/venv/lib/python3.8/site-packages/rasa/cli/.

# Switch back to non-root to run code
USER 1001

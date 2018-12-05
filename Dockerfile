############################################################
# Dockerfile to build HApiDoc Containers
# Based on Ubuntu 18.08
############################################################

# Set the base image to Ubuntu
FROM ubuntu:18.04

##### Install libraries/dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        openssh-server

# Install openssl and configure git to avoid https issues
RUN apt-get install openssl
RUN git config --global http.sslVerify false

# Install anaconda2
RUN wget https://repo.continuum.io/archive/Anaconda2-4.4.0-Linux-x86_64.sh
RUN bash Anaconda2-4.4.0-Linux-x86_64.sh -b -p ~/anaconda
RUN rm Anaconda2-4.4.0-Linux-x86_64.sh

# Create alias to use anaconda as python default interpreter
RUN echo 'alias python=/root/anaconda/bin/python' >> ~/.bashrc
RUN ["/bin/bash", "-c", "source ~/.bashrc"]

# Manually add the path to Anaconda
RUN echo 'export PATH=~/anaconda/bin:$PATH' >> ~/.bashrc
RUN ["/bin/bash", "-c", "source ~/.bashrc"]
env PATH ~/anaconda/bin:$PATH
RUN echo $PATH
RUN ["/bin/bash", "-c", "conda update --yes conda"]
RUN ["/bin/bash", "-c", "conda config --add channels hugo"]
RUN ["/bin/bash", "-c", "conda config --add channels conda-forge"]
RUN ["/bin/bash", "-c", "conda config --add channels kpurdon"]

# Install project python dependencies using conda
ADD ./requirements.txt ./requirements.txt
RUN ["/bin/bash", "-c", "conda install --yes --file requirements.txt"]

# Create dir for project (remove dir if exists)
RUN rm -rf hapidocweb
RUN mkdir hapidocweb

# Set project directory
ENV DIRPATH /hapidocweb

# Create logs directory
RUN mkdir $DIRPATH/logs
RUN chmod +x $DIRPATH/logs

# Set the default directory where CMD, RUN, and ENTRYPOINT commands will execute
WORKDIR $DIRPATH

# copy local files
ADD app ./app
ADD mappings.py ./mappings.py
ADD run.py ./run.py

# make script executable
RUN chmod +x ./run.py

# Download required js files
ADD https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js app/static/js/jquery.min.js
ADD https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js app/static/js/jquery-ui.min.js
ADD https://raw.githubusercontent.com/twitter/typeahead.js/master/dist/typeahead.bundle.js app/static/js/typeahead.js

# Run the command on container startup
CMD /root/anaconda/bin/python ./run.py
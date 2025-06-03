# Build this image on a Python 3.12 image
#FROM python:3.12

#lightweight version of python
FROM python:3.12-slim 

#EXPOSE 5001

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends build-essential git curl && \
#     rm -rf /var/lib/apt/lists/*

WORKDIR /server


# Copy requirements.txt in so that pip can access it
COPY requirements.txt requirements.txt

# Install the requirements.txt
ENV PYTORCH_INSTALL_ONLY_CPU=1
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt


COPY . .

CMD ["python","server.py"]
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container

# Copy the current directory contents into the container at /usr/src/app

# Install any needed packages specified in requirements.txt
# RUN apt-get install espeak-ng
ADD requirements.txt requirements.txt
ADD install.sh install.sh

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir app

WORKDIR /app
COPY . .


# Run app.py when the container launches
CMD ["/app/start.sh"]


# CMD ["gunicorn", "wsgi:pp", '-b', '0.0.0.0:8000', ]
# ENTRYPOINT [ "python", "flaskApp.py" ]
# EXPOSE 8080
# Use an official Python runtime as a parent image
FROM python:3.10-alpine3.18

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install espeak-ng

# Run app.py when the container launches
CMD ["gunicorn", "wsgi:app", '-b', '0.0.0.0:5000', ]
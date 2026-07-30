#docker #devops #coding #apps #dev 

[[Docker]]


how do i change the listening port for my container?
To change the listening port for your container, you need to modify both the application inside the container to listen on a different port and the Docker configuration to map the new port. Here’s how you can do it:

1. Change the Application's Listening Port
First, ensure that your application is configured to listen on the desired port. This change depends on the application and the framework you are using. For example, if you are using a Flask application, you might change the port in your application code or configuration file:

# Example for a Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=NEW_PORT)
2. Update the Dockerfile
If your application listens on a different port, update the EXPOSE instruction in your Dockerfile to reflect this change. This step is optional but recommended for documentation purposes:

# Expose the new port
EXPOSE NEW_PORT
3. Update the Docker Run Command or Docker Compose File
When you run the container, you need to map the new container port to a host port. You can do this using the -p flag with docker run or by updating your docker-compose.yml file.

Using docker run

docker run -d -p HOST_PORT:NEW_PORT <image-name>
HOST_PORT: The port on your host machine you want to use to access the application.
NEW_PORT: The new port your application is listening on inside the container.
Using Docker Compose

Update the ports section in your docker-compose.yml file:

version: '3.4'

services:
  certtrack:
    image: certtrack
    build:
      context: .
      dockerfile: ./Dockerfile
    ports:
      - HOST_PORT:NEW_PORT
4. Rebuild and Restart the Container
After making these changes, rebuild your Docker image and restart the container to apply the new configuration:

# If using Docker Compose
docker-compose up --build

# If using docker run
docker build -t <image-name> .
docker run -d -p HOST_PORT:NEW_PORT <image-name>
Important Considerations
Consistency: Ensure that the port changes are consistent across your application code, Dockerfile, and Docker configuration.
Firewall and Security: Make sure that the new host port is open and accessible if you are running the container in an environment with firewall rules.
Environment Variables: If your application uses environment variables to set the port, ensure they are correctly set in your Docker configuration.
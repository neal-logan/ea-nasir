# https://www.docker.com/blog/supercharging-ai-ml-development-with-jupyterlab-and-docker/

FROM jupyter/base-notebook

# Copy in project methods library into image
COPY ./methods ./methods

# Copy requirements into image
COPY requirements.txt .

# Update pip, install requirements
RUN pip install --upgrade pip
RUN python -m pip install --no-cache -r requirements.txt

# Expose port to serve from
EXPOSE 8888

# Keep container running
CMD ["bash"]
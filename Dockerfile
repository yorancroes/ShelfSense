FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Update and upgrade apt-get, then install necessary dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        libgl1-mesa-dev \
        libxkbcommon-x11-0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-xinerama0 \
        libxcb-xinput0 \
        libxcb-xfixes0 \
        libxcb-shape0 \
        libxcb-render0 \
        libxcb-glx0 \
        libxi6 \
        libxkbfile1 \
        libxcb-cursor0 \
        libglib2.0-0 \
        libglib2.0-dev \
        libdbus-1-3 \
        qtbase5-dev  # This package will pull in the necessary Qt5 libraries

# Set environment variables for Qt
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins
ENV QT_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins
ENV DISPLAY=host.docker.internal:0

# Copy the requirements file into the container
COPY app/requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the port the app runs on (if needed)
EXPOSE 5000

# Run the application
CMD ["python", "app/main.py"]

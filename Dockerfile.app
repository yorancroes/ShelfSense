
FROM python:3.9

# Set working directory
WORKDIR /shelfsense

# Copy application code
COPY . /shelfsense

# Install system dependencies for Qt (Wayland, X11) for Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    libegl1 \
    libgl1-mesa-dev \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libwayland-client0 \
    libwayland-server0 \
    qt6-base-dev \
    qt6-wayland \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Set environment variables for platform detection
# Default to X11 (Linux), macOS and Windows should not need extra settings
RUN if [ "$(uname)" = "Linux" ]; then \
      if [ -n "$WAYLAND_DISPLAY" ]; then \
        export QT_QPA_PLATFORM=wayland; \
      elif [ -n "$DISPLAY" ]; then \
        export QT_QPA_PLATFORM=xcb; \
      fi; \
    elif [ "$(uname)" = "Darwin" ]; then \
      export QT_QPA_PLATFORM=cocoa; \
    else \
      export QT_QPA_PLATFORM=windows; \
    fi

# Set environment variable for XDG runtime dir (required by Wayland)
ENV XDG_RUNTIME_DIR=/tmp/xdg

# Create Wayland runtime directory
RUN mkdir -p /tmp/xdg && chmod 700 /tmp/xdg

# Set the default command to run the application
CMD ["python", "app/main.py"]


FROM python:3.9

# Arguments for platform-specific builds
ARG TARGETPLATFORM
ARG BUILDPLATFORM

# Install platform-specific dependencies
RUN case "${TARGETPLATFORM:-linux/amd64}" in \
    "linux/amd64"|"linux/arm64") \
        apt-get update && apt-get install -y \
        python3-pyqt5 \
        python3-pyqt5.qtwebengine \
        libqt5gui5 \
        libqt5webengine5 \
        libqt5webenginewidgets5 \
        libxcb1 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-shm0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 \
        libxcb-cursor0 \
        x11-utils \
        ;; \
    "windows/amd64") \
        echo "Windows build - no additional system packages required" \
        ;; \
    "darwin/amd64"|"darwin/arm64") \
        echo "macOS dependencies should be installed using Homebrew or a macOS-compatible method" \
        ;; \
    *) echo "Unsupported platform: ${TARGETPLATFORM}" && exit 1 ;; \
    esac \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /shelfsense
COPY app/requirements.txt /shelfsense/app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt
COPY . .
CMD ["python", "app/main.py"]

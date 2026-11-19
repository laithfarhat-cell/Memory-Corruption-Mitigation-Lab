FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev libasan8 libubsan1 rustc gdb make python3-venv && rm -rf /var/lib/apt/lists/*
WORKDIR /lab
COPY requirements.txt .
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:${PATH}"
COPY . .
RUN make clean && make all && make test
CMD ["make", "audit"]

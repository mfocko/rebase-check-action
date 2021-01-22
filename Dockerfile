FROM fedora:33
RUN dnf install -y git-core
COPY check-rebase.py /check-rebase.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

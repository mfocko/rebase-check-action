FROM docker.io/usercont/base
COPY check-rebase.py /check-rebase.py
ENTRYPOINT ["/check-rebase.py"]

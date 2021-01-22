FROM fedora:33

COPY check-rebase.py /check-rebase.py

ENTRYPOINT ["/check-rebase.py"]

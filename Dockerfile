FROM alpine:latest
RUN apk add bash git python3
COPY check-rebase.py /check-rebase.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

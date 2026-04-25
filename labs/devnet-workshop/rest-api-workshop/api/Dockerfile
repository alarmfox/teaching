FROM golang:1.22.3-alpine3.18 as build

WORKDIR /src

COPY main.go .

RUN go build -o api main.go

FROM scratch

WORKDIR /app
COPY --from=build /src/api .

CMD ["/app/api"]

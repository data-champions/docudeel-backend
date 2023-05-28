## Example backend
Scaffolding for a backend processing a file + some params.

Start
```
make build_and_run
```

Example requests
```
make send_good_request
make send_bad_request
```

docker build . -tag docudeel
docker run --env-file ./env.docker -it docudeel 


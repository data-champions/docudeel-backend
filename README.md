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



# to update contacts
Modify only `"data/Kopie van clean_relaties(1) updated.xlsx"` and run 
`python data/update_client_db.py` to update files.
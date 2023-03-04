
send_wrong_debit_request: 
	# data.json could be any file  (pdf, png, zip)
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@data.json" -F "user_id=yooo" \
		-F "email=pizaaa" -F "description=invoice_n2" \
		-F "lang=nl" \
		http://127.0.0.1:5000/

send_good_request: 
	# data.json could be any file  (pdf, png, zip)
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@data/data.json" -F "user_id=13032AI" \
		-F "email=pizaaa" -F "description=invoice_n2" \
		-F "lang=nl" \
		http://127.0.0.1:5000/

send_bad_request: 
	# data.json could be any file  (pdf, png, zip)
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@data/data.json" -F "user_id=yooo" \
		-F "email=pizaaa" \
		http://127.0.0.1:5000/

send_good_request_server: 
	# data.json could be any file  (pdf, png, zip)
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@data/Slides.pptx" -F "user_id=yooo" \
		-F "email=pizaaa" -F "description=invoice_n2" \
		https://docudeel-backend.als8v4i7d204u.eu-central-1.cs.amazonlightsail.com/



send_bad_request_server: 
	# data.json could be any file  (pdf, png, zip)
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@data/see-thru.pdf" -F "user_id=yooo" \
		-F "email=pizaaa" \
		https://docudeel-backend.als8v4i7d204u.eu-central-1.cs.amazonlightsail.com/




build_and_run:
	docker-compose up -d --build &&  docker logs --follow pyflaskfileupload
# https://examples.javacodegeeks.com/upload-a-file-with-python-flask/


# -- to create the image and start container --
# docker-compose up -d --build
 
# -- to check if the container is started
# docker ps -a
 
# -- to stop and remove the container --
# docker-compose down
 
# -- to view the container logs --
# docker logs --follow pyflaskfileupload
 
# -- to remove the created image --
# docker rmi pyflaskfileupload
setup:
	pip install -r requirements.txt

setup-docker:
	pip install -r requirements.txt --no-cache-dir

check_branch_updated:
	python infra/check_latest_main.py
run:
	python src/app.py
deploy:
	python infra/deploy.py

test:
	python infra/env_check.py
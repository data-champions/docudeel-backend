
send_good_request: 
	# data.json could be any file  (pdf, png, zip)
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@data.json" -F "user_id=yooo" \
		-F "email=pizaaa" -F "description=invoice_n2" \
		http://127.0.0.1:5000/



send_bad_request: 
	# data.json could be any file  (pdf, png, zip)
	curl -i -X POST -H "Content-Type: multipart/form-data" \
		-F "file=@data.json" -F "user_id=yooo" \
		-F "email=pizaaa" \
		http://127.0.0.1:5000/


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
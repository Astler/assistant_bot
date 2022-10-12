docker stop admin.test
docker rm admin.test

app="cat.bot"
docker build -t ${app} .
docker run -d -p 499998:49998 \
  --name=${app} \
  -v "$PWD":/app ${app}
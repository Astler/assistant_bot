docker stop cat.bot
docker rm cat.bot

app="cat.bot"
docker build -t ${app} .
docker run -m 2g -it -p 49998:49998 \
  --name=${app} \
  -v "$PWD":/app ${app}
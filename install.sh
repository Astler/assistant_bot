docker stop cat.bot
docker rm cat.bot

app="cat.bot"
docker build -t ${app} .
docker run -it -d -p 49998:49998 \
  --name=${app} \
  -v "$PWD":/app ${app}
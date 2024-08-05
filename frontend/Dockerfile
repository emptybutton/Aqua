FROM node:20.16.0-alpine3.19

WORKDIR /aqua

COPY . .

RUN npm install -g typescript && npm install -g sass
CMD ["ash", "./scripts/start.sh"]

FROM node:alpine3.19

WORKDIR /aqua

COPY . .

RUN npm install -g typescript
CMD ["tsc", "-w"]

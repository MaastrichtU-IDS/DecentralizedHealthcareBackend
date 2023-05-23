FROM node:16

WORKDIR /usr/src/js

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8888

CMD ["node", "src/koa/koa.js"]
# RUN node ./src/koa.js
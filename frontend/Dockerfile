FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install @vue/cli@5.0.8 -g
RUN npm install -g postcss-loader postcss postcss-import postcss-url
RUN npm install -g serve

COPY package.json .
COPY package-lock.json .
RUN npm install
RUN npm install --save bootstrap-vue

COPY . .

EXPOSE 8080
CMD ["npm", "run", "dev"]

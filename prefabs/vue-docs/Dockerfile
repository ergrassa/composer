FROM node:14 as build-stage
WORKDIR /client
COPY package*.json ./
RUN yarn
COPY ./ .
RUN yarn docs

FROM nginx:alpine
RUN mkdir /app
COPY --from=build-stage /client/docs /app
COPY nginx.conf /etc/nginx/nginx.conf
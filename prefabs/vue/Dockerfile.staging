FROM node:14 as build-stage
WORKDIR /client
COPY package*.json ./
RUN yarn
COPY ./ .
ARG BUILDMODE
RUN yarn build --mode=${BUILDMODE}

FROM nginx
RUN mkdir /app
COPY --from=build-stage /client/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

FROM node:14 as build-stage
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . ./
ARG build_mode
RUN yarn build --mode=${build_mode}

FROM nginx
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
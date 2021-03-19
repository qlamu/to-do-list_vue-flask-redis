FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
ARG VUE_APP_SERVER
ENV VUE_APP_SERVER ${VUE_APP_SERVER}
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine as production-stage
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
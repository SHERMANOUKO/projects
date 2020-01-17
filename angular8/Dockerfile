FROM node:11.6.0-alpine AS builder
COPY . ./plotsapp
WORKDIR /plotsapp
RUN npm i
RUN $(npm bin)/ng build --prod

FROM nginx:1.15.8-alpine
COPY --from=builder /plotsapp/dist/plotsapp/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf






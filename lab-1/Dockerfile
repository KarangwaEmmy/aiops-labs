FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["tail", "-f", "/dev/null"]

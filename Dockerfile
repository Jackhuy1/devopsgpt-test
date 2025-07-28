FROM node:16-alpine as builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --production

COPY --from=builder /app/build ./build
COPY . .

EXPOSE 5000

CMD ["npm", "start"]

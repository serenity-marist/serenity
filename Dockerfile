FROM node:8
WORKDIR /Users/garycoltrane/desktop/projects/capping2/workdir

COPY package*.json ./

RUN npm install


COPY . .

EXPOSE  3000

CMD [ "npm", "start"]

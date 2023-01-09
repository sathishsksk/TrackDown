#Base Image
FROM ghcr.io/arghyac35/aria-telegram-mirror-bot:main

WORKDIR /bot/

RUN npm install

CMD ["npm", "start"]

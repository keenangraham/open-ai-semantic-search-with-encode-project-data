FROM --platform=linux/amd64 node:16.14.0-alpine

ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR /scripts

COPY --chown=nextjs:nextjs scripts .

RUN chmod -R +x /scripts

WORKDIR /ssed

COPY /frontend/package*.json ./

RUN npm ci

COPY /frontend/. .

RUN npm run build

EXPOSE 3000

ENTRYPOINT ["/scripts/entrypoint.sh"]

CMD ["npm", "run", "start"]
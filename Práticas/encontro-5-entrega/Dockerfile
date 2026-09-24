FROM node:22-bookworm-slim
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY --chown=node:node server.js ./
ARG RELEASE=v1
COPY --chown=node:node releases/${RELEASE}.json ./release.json
ENV NODE_ENV=production
USER node
EXPOSE 3000
CMD ["node", "server.js"]

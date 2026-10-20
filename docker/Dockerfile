# syntax=docker/dockerfile:1
# ─── CGRF Header ───────────────────────────────────────────────
# File: docker/Dockerfile
# Stage: 11_COMMIT
# SRS: SRS-CN-ENTERTAINMENT-BUILD-001
# CAPS: pending
# CK: pending
# Dispatch: DISP-BUILD-entertainment
# Seat: BITS-CODEGEN
# Owner: Citadel Nexus Inc.
# Created: 2026-10-20
# Depends: package.json, tsconfig.build.json
# EnumType: ConfigDoc
# EnumEdges: DEPENDS_ON package.json; DEPENDS_ON tsconfig.build.json
# DAG Node: none
# Intent: Build the compiled guild using ephemeral registry credentials without retaining tokens in image layers.
# ───────────────────────────────────────────────────────────────

FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
# The temporary npm config and credential are mounted only for installation.
RUN --mount=type=secret,id=node_auth_token,required=true \
    --mount=type=tmpfs,target=/run/npm \
    sh -eu -c 'printf "%s\n" "@citadel-guilds:registry=https://npm.pkg.github.com" "//npm.pkg.github.com/:_authToken=$(cat /run/secrets/node_auth_token)" > /run/npm/npmrc; NPM_CONFIG_USERCONFIG=/run/npm/npmrc npm ci'
COPY tsconfig.json tsconfig.build.json ./
COPY src ./src
RUN npm run build && npm prune --omit=dev --ignore-scripts

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER node
EXPOSE 8400
CMD ["node", "dist/index.js"]

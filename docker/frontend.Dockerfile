# =============================================================================
# SkillBridge AI — Frontend Dockerfile
# =============================================================================
# Node 22 Alpine for the React + Vite frontend dev server.
# =============================================================================

FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy application code
COPY frontend/ .

# Expose Vite dev server port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=45s \
    CMD wget -qO- http://localhost:5173 || exit 1

# Run Vite dev server (accessible from Docker network)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Stacks Suportadas Embrapa I/O

## 🎯 Visão Geral

Este documento detalha as stacks tecnológicas suportadas pelo módulo Embrapa I/O, com padrões, exemplos e melhores práticas para cada uma.

## 📦 Stack 1: Node.js + Express + MongoDB

### Versões Recomendadas
- Node.js: 20.x LTS
- Express: 4.x
- MongoDB: 7.x
- Mongoose: 8.x

### Estrutura de Projeto

```
projeto/
├── src/
│   ├── index.js
│   ├── routes/
│   │   └── api.routes.js
│   ├── models/
│   │   └── User.model.js
│   ├── controllers/
│   │   └── user.controller.js
│   ├── middleware/
│   │   ├── auth.middleware.js
│   │   └── error.middleware.js
│   └── config/
│       ├── database.js
│       ├── sentry.js
│       └── matomo.js
├── docker-compose.yaml
├── .env.example
├── .env.io.example
├── package.json
└── .embrapa/settings.json
```

### docker-compose.yaml

```yaml
services:
  api:
    build: .
    restart: unless-stopped
    ports:
      - "${NODEJS_PORT}:3000"
    environment:
      NODE_ENV: production
      MONGODB_URI: mongodb://mongo:27017/${DB_NAME}
      SENTRY_DSN: ${SENTRY_DSN}
    networks:
      - stack
    depends_on:
      mongo:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "--quiet", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  mongo:
    image: mongo:7-jammy
    restart: unless-stopped
    environment:
      MONGO_INITDB_DATABASE: ${DB_NAME}
    volumes:
      - mongo_data:/data/db
    networks:
      - stack
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  stack:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
    external: true

volumes:
  mongo_data:
    name: ${MONGO_VOLUME}
    external: true
```

---

## 📦 Stack 2: Node.js + Express + PostgreSQL

### Versões Recomendadas
- Node.js: 20.x LTS
- Express: 4.x
- PostgreSQL: 17.x
- Sequelize: 6.x

### docker-compose.yaml (diferenças)

```yaml
services:
  db:
    image: postgres:17-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - stack
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    name: ${POSTGRES_VOLUME}
    external: true
```

---

## 📦 Stack 3: Vue.js + Vuetify (Frontend)

### Versões Recomendadas
- Vue.js: 3.x
- Vuetify: 3.x
- Vite: 5.x
- Axios: 1.x
- Dexie.js: 4.x (PWA)

### Estrutura de Projeto

```
projeto/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   │   └── index.js
│   ├── store/
│   │   └── index.js
│   ├── views/
│   │   ├── Home.vue
│   │   └── About.vue
│   ├── components/
│   │   └── HelloWorld.vue
│   ├── plugins/
│   │   ├── vuetify.js
│   │   ├── sentry.js
│   │   └── matomo.js
│   └── assets/
│       └── logo-embrapa.png
├── public/
├── docker-compose.yaml
├── vite.config.js
├── package.json
└── .embrapa/settings.json
```

### docker-compose.yaml

```yaml
services:
  frontend:
    build: .
    restart: unless-stopped
    ports:
      - "${VUE_PORT}:80"
    environment:
      VITE_API_URL: ${API_URL}
      VITE_SENTRY_DSN: ${SENTRY_DSN}
      VITE_MATOMO_ID: ${MATOMO_ID}
    networks:
      - stack
    healthcheck:
      test: ["CMD", "wget", "--spider", "--quiet", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  stack:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
    external: true
```

### Tema Embrapa (Vuetify)

```javascript
// plugins/vuetify.js
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'embrapa',
    themes: {
      embrapa: {
        dark: false,
        colors: {
          primary: '#008542',    // Verde Embrapa
          secondary: '#6FAC46',  // Verde claro
          accent: '#FFB81C',     // Amarelo
          error: '#D32F2F',
          info: '#1976D2',
          success: '#388E3C',
          warning: '#F57C00',
        },
      },
    },
  },
})
```

---

## 📦 Stack 4: React (Frontend)

### Versões Recomendadas
- React: 18.x
- Vite: 5.x
- React Router: 6.x
- Material-UI: 5.x (opcional)

### docker-compose.yaml (similar ao Vue.js)

```yaml
services:
  frontend:
    build: .
    restart: unless-stopped
    ports:
      - "${REACT_PORT}:80"
    environment:
      VITE_API_URL: ${API_URL}
      VITE_SENTRY_DSN: ${SENTRY_DSN}
    networks:
      - stack
```

---

## 📦 Stack 5: React Native (Mobile)

### Versões Recomendadas
- React Native: Latest
- Expo: Latest (opcional)

### docker-compose.yaml (Backend de suporte)

```yaml
services:
  mobile-backend:
    build: ./backend
    restart: unless-stopped
    ports:
      - "${API_PORT}:3000"
    networks:
      - stack
```

---

## 📦 Stack 6: .NET Blazor

### Versões Recomendadas
- .NET: 8.x
- Entity Framework Core: 8.x

### docker-compose.yaml

```yaml
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "${DOTNET_PORT}:8080"
    environment:
      ASPNETCORE_ENVIRONMENT: ${IO_STAGE}
      ConnectionStrings__DefaultConnection: ${CONNECTION_STRING}
      Sentry__Dsn: ${SENTRY_DSN}
    networks:
      - stack
    healthcheck:
      test: ["CMD", "wget", "--spider", "--quiet", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## 📦 Stack 7: PHP + Laravel + MySQL

### Versões Recomendadas
- PHP: 8.2
- Laravel: 10.x
- MySQL: 8.x
- Composer: 2.x

### docker-compose.yaml

```yaml
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "${PHP_PORT}:80"
    environment:
      APP_ENV: ${IO_STAGE}
      DB_CONNECTION: mysql
      DB_HOST: db
      DB_DATABASE: ${DB_NAME}
      DB_USERNAME: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    networks:
      - stack
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: mysql:8
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - stack
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  stack:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
    external: true

volumes:
  mysql_data:
    name: ${MYSQL_VOLUME}
    external: true
```

### Dockerfile (Laravel)

```dockerfile
FROM php:8.2-apache

# Instalar extensões PHP necessárias
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zip \
    unzip \
    curl \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo pdo_mysql

# Habilitar mod_rewrite
RUN a2enmod rewrite

# Copiar código da aplicação (⚠️ NÃO usar bind mount!)
COPY . /var/www/html/

# Ajustar permissões
RUN chown -R www-data:www-data /var/www/html/ \
    && chmod -R 755 /var/www/html/storage

WORKDIR /var/www/html
```

---

## 📦 Stack 8: PHP + PostgreSQL (Legado/Genérico)

### Versões Recomendadas
- PHP: 8.2
- PostgreSQL: 17.x
- Apache: 2.4

### Estrutura de Projeto

```
projeto/
├── src/                      # Código PHP
│   ├── index.php
│   ├── config/
│   │   └── database.php
│   └── ...
├── database/                 # Scripts SQL (serão copiados via Dockerfile)
│   ├── init.sql
│   └── seed.sql
├── uploads/                  # Diretório para uploads (volume externo)
├── docker-compose.yaml
├── Dockerfile
├── Dockerfile.db             # Dockerfile para PostgreSQL com scripts
├── .dockerignore
├── .env.example
├── .env.io.example
└── .embrapa/settings.json
```

### docker-compose.yaml

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "${APP_PORT}:80"
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      APP_URL: ${APP_URL}
      SENTRY_DSN: ${SENTRY_DSN}
      MATOMO_ID: ${MATOMO_ID}
      IO_PROJECT: ${IO_PROJECT}
      IO_APP: ${IO_APP}
      IO_STAGE: ${IO_STAGE}
      IO_VERSION: ${IO_VERSION}
    volumes:
      - app_uploads:/var/www/html/uploads    # Volume externo para uploads
    networks:
      - stack
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health.php"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    build:
      context: .
      dockerfile: Dockerfile.db
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data    # Volume externo para dados
    networks:
      - stack
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Serviços CLI obrigatórios
  backup:
    build:
      context: .
      dockerfile: Dockerfile.db
    restart: "no"
    profiles:
      - cli
    environment:
      PGPASSWORD: ${DB_PASSWORD}
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      IO_PROJECT: ${IO_PROJECT}
      IO_APP: ${IO_APP}
      IO_STAGE: ${IO_STAGE}
      IO_VERSION: ${IO_VERSION}
    volumes:
      - backup_data:/backup
    networks:
      - stack
    command: >
      sh -c "
        set -ex &&
        BACKUP_DIR=${IO_PROJECT}_${IO_APP}_${IO_STAGE}_${IO_VERSION}_$$(date +'%Y-%m-%d_%H-%M-%S') &&
        mkdir -p /backup/$$BACKUP_DIR &&
        pg_dump -h db -U ${DB_USER} -d ${DB_NAME} > /backup/$$BACKUP_DIR/database.sql &&
        tar -czf /backup/$$BACKUP_DIR.tar.gz -C /backup $$BACKUP_DIR &&
        rm -rf /backup/$$BACKUP_DIR &&
        echo 'Backup completed: '$$BACKUP_DIR'.tar.gz'
      "

  restore:
    build:
      context: .
      dockerfile: Dockerfile.db
    restart: "no"
    profiles:
      - cli
    environment:
      PGPASSWORD: ${DB_PASSWORD}
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
      BACKUP_FILE_TO_RESTORE: ${BACKUP_FILE_TO_RESTORE:-no_file}
    volumes:
      - backup_data:/backup
    networks:
      - stack
    command: >
      sh -c "
        set -ex &&
        test -f /backup/${BACKUP_FILE_TO_RESTORE} &&
        RESTORE_DIR=$$(mktemp -d) &&
        tar -xf /backup/${BACKUP_FILE_TO_RESTORE} -C $$RESTORE_DIR --strip-components=1 &&
        psql -h db -U ${DB_USER} -d ${DB_NAME} < $$RESTORE_DIR/database.sql &&
        rm -rf $$RESTORE_DIR &&
        echo 'Restore completed from: ${BACKUP_FILE_TO_RESTORE}'
      "

  sanitize:
    build:
      context: .
      dockerfile: Dockerfile.db
    restart: "no"
    profiles:
      - cli
    environment:
      PGPASSWORD: ${DB_PASSWORD}
      DB_NAME: ${DB_NAME}
      DB_USER: ${DB_USER}
    networks:
      - stack
    command: >
      sh -c "
        set -ex &&
        psql -h db -U ${DB_USER} -d ${DB_NAME} -c 'VACUUM ANALYZE;' &&
        echo 'Database optimized successfully'
      "

networks:
  stack:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}
    external: true

volumes:
  postgres_data:
    name: ${POSTGRES_VOLUME}
    external: true
  app_uploads:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_uploads
    external: true
  backup_data:
    name: ${IO_PROJECT}_${IO_APP}_${IO_STAGE}_backup
    external: true
```

### Dockerfile (Aplicação PHP)

```dockerfile
FROM php:8.2-apache

# Instalar extensões PHP necessárias para PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && docker-php-ext-install pdo pdo_pgsql pgsql \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Habilitar mod_rewrite
RUN a2enmod rewrite

# Configurar DocumentRoot se necessário
# ENV APACHE_DOCUMENT_ROOT /var/www/html/public
# RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf

# ⚠️ IMPORTANTE: Copiar código da aplicação (NÃO usar bind mount!)
COPY . /var/www/html/

# Ajustar permissões
RUN chown -R www-data:www-data /var/www/html/ \
    && chmod -R 755 /var/www/html/

# Criar diretório de uploads (será montado como volume externo)
RUN mkdir -p /var/www/html/uploads \
    && chown www-data:www-data /var/www/html/uploads

WORKDIR /var/www/html

EXPOSE 80
```

### Dockerfile.db (PostgreSQL com scripts de inicialização)

```dockerfile
FROM postgres:17-alpine

# ⚠️ IMPORTANTE: Copiar scripts SQL (NÃO usar bind mount!)
# Scripts são executados automaticamente em ordem alfabética
COPY ./database/*.sql /docker-entrypoint-initdb.d/
```

### .dockerignore

```
# Arquivos que NÃO devem ser copiados para a imagem
.git
.gitignore
.env
.env.io
.env.example
.env.io.example
docker-compose.yaml
docker-compose.yml
Dockerfile
Dockerfile.*
.dockerignore
*.md
*.log
.idea
.vscode
node_modules
vendor
tests
```

### Notas Importantes

1. **Código da aplicação**: Copiado via `COPY` no Dockerfile, nunca via bind mount
2. **Scripts de banco**: Copiados via `COPY` no Dockerfile.db para `/docker-entrypoint-initdb.d/`
3. **Uploads**: Volume externo para dados dinâmicos que precisam persistir
4. **Backup**: Volume externo dedicado para armazenar backups
5. **.dockerignore**: Essencial para evitar copiar arquivos desnecessários

---

## 🔄 Matriz de Compatibilidade

| Stack | Banco Suportado | Integrações | Difficulty |
|-------|----------------|-------------|------------|
| Node.js + Express + MongoDB | MongoDB | Sentry, Matomo | ⭐⭐ |
| Node.js + Express + PostgreSQL | PostgreSQL | Sentry, Matomo | ⭐⭐ |
| Vue.js + Vuetify | N/A | Sentry, Matomo | ⭐⭐ |
| React | N/A | Sentry, Matomo | ⭐⭐ |
| React Native | N/A | Sentry | ⭐⭐⭐ |
| .NET Blazor | SQL Server, PostgreSQL | Sentry | ⭐⭐⭐ |
| PHP + Laravel + MySQL | MySQL | Sentry, Matomo | ⭐⭐ |
| PHP + PostgreSQL (Legado) | PostgreSQL | Sentry, Matomo | ⭐⭐ |

---

**Versão**: 1.1
**Última atualização**: 2026-01-20
**Autor**: Módulo Embrapa I/O BMAD

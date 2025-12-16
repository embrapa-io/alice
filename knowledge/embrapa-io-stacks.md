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

## 📦 Stack 7: PHP + Laravel

### Versões Recomendadas
- PHP: 8.2
- Laravel: 10.x
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

volumes:
  mysql_data:
    name: ${MYSQL_VOLUME}
    external: true
```

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
| PHP + Laravel | MySQL, PostgreSQL | Sentry | ⭐⭐ |

---

**Versão**: 1.0
**Última atualização**: 2025-12-15
**Autor**: Módulo Embrapa I/O BMAD

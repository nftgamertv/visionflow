# VisionFlow - Enterprise Computer Vision Platform

> End-to-end platform for building production-grade computer vision applications

VisionFlow is an enterprise-native MLOps platform that empowers teams to ingest, annotate, version, train, and deploy computer vision models with unparalleled speed, security, and scalability.

## Features

### P0 (Core Features)
- ✅ **Multi-tenant Architecture** with database-level Row-Level Security (RLS)
- ✅ **Real-time Collaborative Annotation** using Supabase Realtime
- ✅ **Bounding Box Annotation Tool** with Konva.js canvas
- ✅ **Secure Image Upload** via presigned S3/R2 URLs
- ✅ **Dataset Versioning** with preprocessing and augmentation pipelines
- ✅ **Export to Multiple Formats** (COCO, YOLO, VOC)
- ✅ **Enterprise Authentication** with Supabase Auth
- ✅ **Asynchronous Task Processing** with ARQ workers
- ✅ **HIPAA/SOC2 Compliance** architecture

### Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Next.js 15    │──────│   FastAPI       │──────│  PostgreSQL     │
│   App Router    │      │   Backend       │      │  (Supabase)     │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
             ┌──────▼──────┐         ┌─────▼─────┐
             │ ARQ Workers │         │  S3/R2    │
             │  (Redis)    │         │  Storage  │
             └─────────────┘         └───────────┘
```

## Tech Stack

### Frontend
- **Next.js 15** - App Router with Server Components
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Konva.js** - High-performance canvas rendering
- **Supabase SSR** - Authentication and real-time subscriptions

### Backend
- **FastAPI** - High-performance Python API
- **Python 3.11+** - Modern Python features
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - Database ORM
- **Boto3** - S3/R2 storage integration

### Data & Infrastructure
- **Supabase** - PostgreSQL with Auth, Realtime, and Storage
- **Redis** - Task queue and caching
- **ARQ** - Async task processing
- **Docker Compose** - Local development environment
- **pnpm** - Fast, disk-efficient package manager

### Computer Vision
- **Albumentations** - Image augmentation library
- **OpenCV** - Image processing
- **NumPy** - Numerical computing

## Prerequisites

- **Node.js** 18+ and **pnpm** 8+
- **Python** 3.11+
- **Docker** and **Docker Compose**
- **Supabase CLI** ([installation guide](https://supabase.com/docs/guides/cli))
- **S3-compatible storage** (AWS S3 or Cloudflare R2)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-org/visionflow.git
cd visionflow
```

### 2. Install dependencies

```bash
# Install Node.js dependencies
pnpm install

# Install Python dependencies for API
cd apps/api
pip install -r requirements.txt
cd ../..

# Install Python dependencies for workers
cd apps/workers
pip install -r requirements.txt
cd ../..
```

### 3. Start Supabase

```bash
supabase start
```

This will start the local Supabase stack. Note the output - you'll need the `anon key` and `JWT secret`.

### 4. Configure environment variables

```bash
# Copy example env files
cp .env.example .env
cp apps/web/.env.example apps/web/.env.local
cp apps/api/.env.example apps/api/.env
cp apps/workers/.env.example apps/workers/.env
```

Edit `.env` and set:
- `SUPABASE_ANON_KEY` - from `supabase status`
- `SUPABASE_JWT_SECRET` - from `supabase status`
- `S3_*` variables - your S3/R2 credentials

### 5. Run database migrations

```bash
supabase db reset
```

This will apply all migrations in `supabase/migrations/`.

### 6. Start the development stack

```bash
# Option 1: Using Docker Compose (recommended)
docker-compose up

# Option 2: Manual start
# Terminal 1: Next.js
cd apps/web && pnpm dev

# Terminal 2: FastAPI
cd apps/api && uvicorn app.main:app --reload

# Terminal 3: ARQ Workers
cd apps/workers && arq app.main.WorkerSettings
```

### 7. Open the application

- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Supabase Studio**: http://localhost:54323

## Project Structure

```
visionflow/
├── apps/
│   ├── web/                 # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/         # App Router pages
│   │   │   ├── components/  # React components
│   │   │   └── utils/       # Utilities
│   │   └── package.json
│   ├── api/                 # FastAPI backend
│   │   ├── app/
│   │   │   ├── core/        # Config, database
│   │   │   ├── routers/     # API endpoints
│   │   │   ├── models/      # Pydantic models
│   │   │   ├── services/    # Business logic
│   │   │   └── dependencies/# Auth, etc.
│   │   └── requirements.txt
│   └── workers/             # ARQ background workers
│       ├── app/
│       │   └── tasks/       # Task definitions
│       └── requirements.txt
├── packages/
│   ├── shared-types/        # Shared TypeScript types
│   ├── ui/                  # Shared React components
│   ├── eslint-config-custom/
│   └── typescript-config-custom/
├── supabase/
│   ├── migrations/          # Database migrations
│   └── config.toml
├── docker-compose.yml
├── pnpm-workspace.yaml
└── package.json
```

## Development Workflow

### Database Changes

1. Create a new migration:
```bash
supabase migration new your_migration_name
```

2. Edit the migration file in `supabase/migrations/`

3. Apply migrations:
```bash
supabase db reset
```

### Type Generation

The project uses a "single source of truth" approach - Pydantic models in the API generate TypeScript types:

```bash
# Export OpenAPI schema
cd apps/api
python -c "from app.main import app; import json; print(json.dumps(app.openapi()))" > ../../packages/shared-types/openapi.json

# Generate Zod schemas
cd packages/shared-types
pnpm run generate-types
```

### Adding New Features

1. **Backend**: Create API endpoints in `apps/api/app/routers/`
2. **Frontend**: Create components in `apps/web/src/components/`
3. **Workers**: Create async tasks in `apps/workers/app/tasks/`

## Security

### Authentication

- JWT-based authentication using Supabase Auth
- Tokens are validated locally in FastAPI for performance
- No credentials stored in frontend code

### Authorization

- **Multi-tenancy**: Enforced at database level with RLS
- **RBAC**: Project-level roles (admin, reviewer, labeler)
- All queries are scoped to user's workspace

### Data Protection

- All data in transit encrypted with TLS 1.2+
- Data at rest encrypted with AES-256
- Presigned URLs for secure uploads
- Connection pooling via Pgbouncer (required for production)

## Performance

### Optimization Strategies

1. **Database**:
   - Indexed columns for fast queries
   - Hybrid schema (relational + JSONB)
   - Connection pooling via Pgbouncer
   - Designed for 1B+ row tables

2. **API**:
   - Async FastAPI for high concurrency
   - Local JWT validation (no network calls)
   - Presigned URLs for direct S3 uploads

3. **Frontend**:
   - Next.js SSR for fast page loads
   - Konva.js for canvas performance
   - Real-time updates via WebSockets

## Testing

```bash
# Frontend tests
pnpm --filter web test

# Backend tests
cd apps/api
pytest

# E2E tests
pnpm --filter e2e-tests test
```

## Deployment

### Production Checklist

- [ ] Set `DATABASE_URL` to use Pgbouncer port (6543, not 5432)
- [ ] Enable PITR on Supabase
- [ ] Configure CORS origins
- [ ] Set up S3/R2 bucket with proper permissions
- [ ] Enable SSL/TLS
- [ ] Configure monitoring and logging
- [ ] Run security audit

### Deployment Targets

- **Frontend**: Vercel (recommended) or Docker
- **Backend**: Kubernetes with FastAPI pods
- **Workers**: Kubernetes with ARQ workers
- **Database**: Supabase Cloud (production tier)

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

Proprietary - All rights reserved

## Support

For issues and questions:
- GitHub Issues: https://github.com/your-org/visionflow/issues
- Documentation: https://docs.visionflow.com

---

Built with ❤️ for enterprise computer vision teams

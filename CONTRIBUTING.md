# Contributing to VisionFlow

Thank you for your interest in contributing to VisionFlow!

## Development Setup

Please follow the [Quick Start guide](README.md#quick-start) in the README to set up your development environment.

## Development Principles

### 1. No Fallbacks, No Mock Data

**CRITICAL**: This project operates under a strict "real data or fail" policy:

- ❌ NO placeholder data
- ❌ NO mock responses
- ❌ NO test data in production code
- ❌ NO fallback values
- ✅ Real functional code only
- ✅ Proper error handling
- ✅ Fail fast and loud

If a feature isn't ready, it should throw a clear error, not return mock data.

### 2. Type Safety

- All TypeScript code must pass `tsc --noEmit` without errors
- Use Pydantic models for all Python API contracts
- Keep frontend/backend types in sync via OpenAPI generation

### 3. Security First

- Always use RLS policies for data access
- Never bypass authentication checks
- Use presigned URLs for file uploads
- Validate all user input

## Code Style

### TypeScript/JavaScript

```typescript
// Use meaningful variable names
const annotationData: BoundingBoxData = { ... }

// Prefer functional components with TypeScript
export function AnnotationCanvas({ imageUrl }: AnnotationCanvasProps) {
  // ...
}

// Use async/await for asynchronous code
const response = await fetch(url)
```

### Python

```python
# Follow PEP 8
# Use type hints
def create_annotation(
    annotation: AnnotationCreate,
    user: AuthenticatedUser,
) -> Annotation:
    # ...

# Use Pydantic for validation
class ProjectCreate(BaseModel):
    name: str
    project_type: str
```

## Git Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests and linting:
   ```bash
   pnpm run lint
   pnpm run type-check
   pnpm run test
   ```

4. Commit with descriptive messages:
   ```bash
   git commit -m "Add bounding box rotation support"
   ```

5. Push and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Process

1. Ensure all CI checks pass
2. Update documentation if needed
3. Add tests for new features
4. Request review from maintainers
5. Address review feedback

## Testing

### Frontend Tests

```bash
pnpm --filter web test
```

### Backend Tests

```bash
cd apps/api
pytest
```

### E2E Tests

```bash
pnpm --filter e2e-tests test
```

## Database Migrations

When making schema changes:

1. Create a new migration:
   ```bash
   supabase migration new your_migration_name
   ```

2. Edit the SQL file in `supabase/migrations/`

3. Test locally:
   ```bash
   supabase db reset
   ```

4. Commit the migration file

## Architecture Decisions

### Why This Tech Stack?

- **Next.js 15**: Best-in-class SSR, App Router, Server Components
- **FastAPI**: High-performance async Python, automatic OpenAPI generation
- **Supabase**: Managed PostgreSQL with Auth, Realtime, and RLS
- **Konva.js**: High-performance canvas for complex annotations
- **ARQ**: Lightweight async task queue, asyncio-native

### Key Patterns

1. **Presigned URLs**: Direct client-to-S3 uploads for scalability
2. **RLS**: Database-level multi-tenancy for security
3. **Real-time**: Supabase Realtime for collaborative features
4. **Hybrid Schema**: Relational columns + JSONB for flexibility
5. **Type Sync**: OpenAPI → Zod schemas for frontend/backend sync

## Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing!

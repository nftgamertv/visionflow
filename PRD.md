 PDF To Markdown Converter
Debug View
Result View
Vision AI Annotation Tool PRD
# Project VisionFlow: Enterprise-Grade

# Computer Vision Platform (PRD &

# Implementation Blueprint)

## Part 1: Platform Charter & Non-Functional

## Requirements

### 1.1. Product Vision & Principles

```
● Vision: To deliver the definitive, end-to-end platform for building production-grade
computer vision. "Project VisionFlow" will empower enterprise teams to ingest, annotate,
version, train, and deploy vision models with unparalleled speed, security, and scalability.
● Mission: This initiative will build a replacement for existing platforms like Roboflow,
establishing a next-generation, enterprise-native MLOps solution.^1 The platform will be
architected from day one to exceed existing feature sets, offering superior collaboration
workflows, advanced 3D/temporal data support, and uncompromising security and
compliance.
● Core Principles:
```
1. **Enterprise-First, Consumer-Grade UX:** All features must be built to enterprise
    standards of security (e.g., SOC2, HIPAA) 2 , scalability, and auditability.^4 This robust
    foundation will be presented through a fast, intuitive, and collaborative user
    experience.
2. **Radical Extensibility:** The platform must function as a central "hub," not an isolated
    "island." This mandates a robust API-first design 5 and deep integration with the
    MLOps ecosystem, including cloud storage (e.g., S3) 7 and orchestration tools (e.g.,
    Kubeflow).^8
3. **Decoupled & Asynchronous Architecture:** A strict separation of concerns is
    mandated. The frontend (Next.js) is decoupled from the API (FastAPI), which is


```
decoupled from long-running jobs (ARQ Workers) 9 and data (S3/Postgres). This
architecture is the key to achieving horizontal scalability and system resilience.
```
4. **Security by Design:** Security is the foundational layer, not an add-on feature.
    Multi-tenancy 10 , granular Role-Based Access Control (RBAC) 11 , and compliance 3
    must be architected at the database level from the initial repository initialization.

### 1.2. Core System Architecture: The Decoupled Stack

This PRD mandates a specific, high-performance architecture. All development must adhere
to this separation of concerns:

1. **Web Application (Client):** Next.js 15 App Router.^12
    ○ **Responsibility:** All UI rendering (Server-Side Rendering/React Server Components),
       client-side state management, user session management (via the Supabase client
       SDK), and executing direct-to-storage file uploads.^14
    ○ The Next.js App Router model allows for the creation of Supabase clients for both
       browser (Client Components) and server (Server Components, Server Actions, Route
       Handlers) contexts, providing a seamless and secure data-fetching model.^13
2. **Core API (Backend):** Python 3.11+ / FastAPI.^15
    ○ **Responsibility:** Serving all business logic, validating Supabase JSON Web Tokens
       (JWTs) 16 , generating presigned URLs for storage 17 , orchestrating asynchronous jobs

(^9) , and managing database transactions.

3. **Database & BaaS:** Supabase (PostgreSQL 16+).^18
    ○ **Responsibility:** Core relational data store (annotations, projects, users),
       Authentication (Supabase Auth) 19 , Real-time collaboration (Supabase Realtime) 20 ,
       and database-level security (Row-Level Security, RBAC).^10
4. **Asynchronous Task Queue:** ARQ (Redis).^9
    ○ **Responsibility:** Executing all long-running, non-blocking jobs. This includes dataset
       augmentations 22 , preprocessing 23 , dataset exports 24 , and any other CPU-intensive
       task that cannot be completed within a standard HTTP request timeout.
5. **ML Services (Orchestration):** FastAPI (as Orchestrator) + Kubeflow (as Executor).^8
    ○ **Responsibility:** The FastAPI backend will _orchestrate_ (not execute) training and
       inference jobs by applying Custom Resource Definitions (CRDs) to a Kubernetes
       cluster running Kubeflow Training Operators.
6. **Object Storage:** S3-Compatible (e.g., AWS S3, Cloudflare R2).^26
    ○ **Responsibility:** Decoupled storage of all raw media (images, videos, point clouds)
       and generated assets (model weights, dataset versions). The database will _only_ store
       pointers (paths) to these objects.


### 1.3. Non-Functional Requirements (NFRs)

These are non-negotiable, P0 requirements for the platform, defining its enterprise-grade
status.^28

```
● Scalability & Performance
○ Core API Latency: All primary API endpoints (e.g., fetching project data, listing
images) must adhere to:
■ p95 < 150ms 29
■ p99 < 500ms 31
○ Page Load Time: The core application shell (post-auth) must achieve:
■ Largest Contentful Paint (LCP) < 2.5 seconds.^32
■ First Input Delay (FID) < 100ms.^32
○ Concurrency (API): The FastAPI backend, deployed with Uvicorn workers, must
support 10,000 concurrent requests 15 without failure. This is facilitated by database
connection pooling.^18
○ Concurrency (Annotation): The Supabase Realtime-backed 20 annotation
workbench must support 50+ concurrent users in a single project session
(viewing/annotating) with cursor/annotation broadcast latency < 100ms.
○ Data Scalability: All database queries must be architected to perform efficiently on
tables containing 1B+ rows (e.g., annotations). This NFR mandates the use of
database partitioning 33 on core tables from the initial schema design.
● Security & Compliance
○ HIPAA / BAA: The platform must be architected to be HIPAA-compliant. This
includes:
■ Signing a Business Associate Agreement (BAA) with Supabase.^3
■ Implementing all customer-side responsibilities of the Supabase shared
responsibility model 37 , including enabling SSL enforcement, network restrictions,
and Point-in-Time Recovery (PITR).
■ Ensuring all data (Protected Health Information - PHI) is encrypted in transit (TLS
1.2+) and at rest (AES-256).^2
○ SOC2 Type 2: The infrastructure must be compliant with SOC2 Type 2 requirements.^2
This will be validated by third-party audit post-launch.
○ GDPR: The platform must adhere to GDPR principles 39 , including:
■ Data Minimization: Only necessary PII is collected.
■ Right to Erasure: A mechanism must be built for workspace admins to
"anonymize" or "delete" a user and their PII, and for users to request data
deletion.
```

```
■ Data Portability: All user-generated data (images, annotations) must be
exportable.
○ Authentication: All API endpoints (excluding public/auth routes) must be protected
and require a valid, locally-validated Supabase JWT.^16
● Data Governance & Auditing
○ Multi-Tenancy: Data must be isolated between tenants (workspaces). This isolation
must be enforced at the database level using PostgreSQL Row-Level Security (RLS).^10
Application-level WHERE tenant_id =... clauses are insufficient and considered a
security failure.
○ RBAC: The platform must support granular, role-based access control (Admin,
Reviewer, Labeler).^11
○ Audit Logs: Comprehensive audit logs must be captured for all significant events.^28
This must be implemented at the database level using the pgaudit extension 47 and at
the application level (API request/response logging). Logs must be stored in a
separate, append-only store.^49
● Reliability & Availability
○ Availability: The platform must maintain 99.99% uptime 4 for all core services (API,
Web App).
○ Disaster Recovery: The database must have Point-in-Time Recovery (PITR) enabled
```
(^3) , with a Recovery Point Objective (RPO) of < 15 minutes.
○ **Error Handling:** The FastAPI backend must implement comprehensive, global error
handling 50 to catch unhandled exceptions and return standardized JSON error
responses, preventing stack trace leakage.

### Table 1.1: Feature Parity & Prioritization Matrix

This table defines the scope of the build, mapping existing Roboflow features to "Project
VisionFlow" and establishing priority. "And Then Some" denotes features that exceed parity.

```
Priority Roboflow Feature Project VisionFlow
Equivalent
```
```
"And Then Some"
Differentiator
```
```
P0 Data Upload
(Images, Video) 1
```
```
Data Ingestion
Service
```
```
Secure, presigned
URL uploads 14 ;
Programmatic
Upload API 51
```

**P0** Annotation Tool
(Box, Polygon,
Keypoint, Class) 52

```
Annotation
Workbench v
```
```
Real-time,
Figma-like
collaboration via
Supabase Realtime
20
```
**P0** Team Roles & Basic
Collaboration 45

```
Identity, Tenancy
& RBAC
```
```
Hardened, DB-level
RLS 10 ; Granular
RBAC 11
```
**P0** Dataset Versioning
(Preprocessing &
Augmentation) 22

```
Data Versioning
Engine
```
```
Decoupled,
non-blocking ARQ
worker 9 ;
albumentations
pipeline 56
```
**P0** Export (COCO,
VOC, YOLO) 24

```
Data Export
Service
```
```
Asynchronous,
queued export jobs
(via ARQ)
```
**P1** One-Click Training
(Roboflow Train) 1

```
ML Training
Service
```
```
Scalable, extensible
orchestration via
Kubeflow 8
```
**P1** Hosted Inference
API 59

```
ML Inference
Service
```
```
Serverless
inference gateway
(FastAPI-based) 61
```
**P1** Model-Assisted
Labeling (Label
Assist) 52

```
Active Learning
Loop v
```
```
Use own trained
models as labeling
assistants.
```
**P1** Annotation
Workflow (Assign,
Review) 52

```
Annotation
Workflow Engine
```
```
Superior,
database-driven
workflow (not
"merging datasets"
```
(^64) )
**P1** (^) Dataset Search 52 **Data Management
Service**
Semantic search &
metadata filtering.


```
P1 Import Integrations
(S3, CVAT, etc.) 7
```
```
Data Ingestion
Service v
```
```
Connect external
S3 buckets; Import
from LabelMe,
CVAT, etc.
```
```
P2 Annotation Insights
(Analytics) 1
```
```
Analytics
Dashboard
```
```
Deeper insights on
labeler productivity
and class
imbalance.
```
```
P2 Roboflow Universe
(Public Datasets) 65
```
```
Public Data
Universe
```
```
Community-driven
repository of
projects and
models.
```
```
P2 Active Learning
(Upload API) 67
```
```
Active Learning
Loop v
```
```
Advanced
strategies: diversity
sampling 69 ,
category-aware 70
```
```
P2 (N/A - New) Advanced Data
Workbench
```
```
3D LiDAR / Point
Cloud Annotation
71
```
```
P2 (N/A - New) Advanced Data
Workbench
```
```
Complex
Temporal Video
Annotation 73
```
```
P0 Security (SOC2,
HIPAA) 2
```
```
Enterprise
Compliance
```
```
Full BAA support,
RLS, pgaudit 47 ,
SAML SSO 75
```
## Part 2: Phase 1 - Repository Initialization & Local

## Environment


### 2.1. Monorepo Scaffolding (pnpm)

```
● Directive: The project must be initialized as a pnpm monorepo.^76 This approach is critical
for managing shared dependencies, especially the shared-types package, and
preventing dependency conflicts and "dependency confusion".^77
● Implementation:
```
1. Initialize the root directory with a package.json and pnpm-workspace.yaml.
2. The pnpm-workspace.yaml must define the workspace packages:
    YAML
    packages:
    - 'apps/*'
    - 'packages/*'
3. Create the initial directory structure as defined in Table 2.1.
4. The root package.json will contain root-level scripts for linting, testing, and building
    the entire monorepo (e.g., pnpm --filter web build).

### Table 2.1: Monorepo Structure

This table defines the non-negotiable directory structure for the "Project VisionFlow"
monorepo.

```
Path Purpose & Tech
```
```
/ Root. Contains pnpm-workspace.yaml, root
package.json, docker-compose.yml,
.github/workflows.
```
```
/apps/web Next.js 15 App: The main frontend
application.^12
```
/apps/api (^) **FastAPI API:** The core Python backend.^15
Contains all API routers, services, and
Pydantic models.^79
/apps/workers **ARQ Workers:** Python service for


```
background jobs.^9 Will import business
logic from apps/api (e.g., augmentation
logic).
```
```
/packages/shared-types Shared Contracts: The single source of
truth for data contracts.^78
```
```
/packages/ui Shared React Components: Common UI
components (buttons, modals, etc.) used
by apps/web.
```
```
/packages/eslint-config-custom Shared ESLint configuration.
```
```
/packages/typescript-config-custom Shared tsconfig.json base.
```
### 2.2. The "Single Source of Truth" Type Contract

The maintenance of separate types for a Python backend (using Pydantic) 81 and a TypeScript
frontend (using Zod) 77 is a primary source of integration bugs in enterprise applications. A
robust, automated workflow is required to eliminate this risk.

The Pydantic models defined in the apps/api codebase are the _single source of truth_ for all
data contracts. FastAPI natively generates a 100% accurate OpenAPI (JSON Schema)
specification from these Pydantic models.^82 This OpenAPI specification will be used to
automatically generate TypeScript-based Zod validation schemas 85 , which the frontend will
consume.

```
● Mandated Workflow:
```
1. The apps/api service will have an internal script (e.g., pnpm --filter api run
    export-schema).
2. This script boots the FastAPI application, generates the openapi.json, and saves it.
3. A second script in packages/shared-types (e.g., pnpm --filter shared-types run
    generate-types) will:
    a. Read the openapi.json from apps/api.
    b. Use an OpenAPI-to-Zod generator (e.g., zod-openapi) to generate schemas.ts,
    which will contain all Zod validation schemas, inside the packages/shared-types
    directory.
4. The apps/web frontend will then import its validation schemas _directly_ from
    @visionflow/shared-types.


5. This ensures the frontend and backend are _always_ in sync. This workflow _must_ be run
    as part of the CI pipeline (see Part 2.4) to catch any breaking changes.

### 2.3. Local Development Environment (Docker Compose)

```
● Directive: All local development must be containerized via docker-compose 86 to ensure
perfect parity with CI and staging environments and to simplify developer onboarding.
● Implementation (docker-compose.yml):
```
1. web: A Dockerfile in apps/web that runs pnpm dev.
2. api: A Dockerfile in apps/api that runs uvicorn main:app --reload.
3. workers: A Dockerfile in apps/workers that runs arq main.WorkerSettings.
4. supabase: Use the official supabase/studio and supabase/postgres images. This
    provides the local Postgres DB, Auth, and Realtime services, managed via the
    Supabase CLI supabase start command, which uses Docker.^87
5. pgbouncer: The Supabase local stack includes pgbouncer.^18 The api and workers
    services _must_ be configured to connect to Postgres _through_ this Pgbouncer port
    (Port 6543), not the direct Postgres port (5432).^88 This is a non-negotiable
    requirement to force developers to use connection pooling from day one. This will
    prevent production-only failures where serverless functions or high-concurrency API
    workers exhaust the Postgres connection limit.^89
6. redis: For ARQ and other caching.

### 2.4. CI/CD Foundation (GitHub Actions)

```
● Directive: A foundational CI pipeline must be established in .github/workflows/ci.yml
before any feature code is written.^92 This pipeline enforces code quality and contract
integrity.
● Implementation: This workflow will trigger on every push and pull_request.
```
1. **Checkout & Setup:** actions/checkout@v4, actions/setup-pnpm,
    actions/setup-python.
2. **Linting (Parallel Jobs):**
    ■ lint-python: Run black --check, isort, and mypy on apps/api and apps/workers.^94
    ■ lint-frontend: Run eslint and prettier --check on apps/web and packages/*.^94
3. **Testing (Parallel Jobs):**
    ■ test-python: Start the docker-compose stack, wait for services, and run pytest in
       apps/api.^97


```
■ test-frontend: Run vitest run in apps/web.^99
```
4. **Type-Check (Build):**
    ■ check-types-frontend: Run pnpm --filter web build (which includes tsc).^94
    ■ check-schema-sync: Run the schema generation workflow from Part 2.2. After
       generation, run git diff --exit-code. If this command finds any uncommitted
       changes, the job will fail. This failure proves the API contract is out of sync and
       _must_ be committed by the developer, preventing integration errors.

## Part 3: Phase 2 - Core Platform & Identity

### 3.1. Database & Schema Foundation

```
● Directive: All database object definitions (tables, roles, RLS policies, functions) must be
managed by Supabase Migrations. Developers must not use the Supabase UI to alter
production schemas.
● Schema Design: The single biggest performance bottleneck for a platform of this type is
the annotations table. A naive JSONB column for all annotation data 101 will be flexible but
will have catastrophic performance, as it is impossible to query or index at scale.^102
Conversely, a purely relational model with separate tables for each annotation type 103 will
be too rigid and complex.
● Mandated Hybrid Schema: A hybrid approach 104 is mandated:
○ Relational for Querying: Core, queryable data (e.g., image_id, class_name,
annotator_id, project_id) will be normalized columns. These columns must be
indexed.
○ JSONB for Flexibility: The actual annotation geometry (e.g., {"x": 10, "y": 20,
"width": 50, "height": 100} or {"points": [...]}) will be stored in a data JSONB
column.^101
○ This architecture allows for fast, indexed queries (e.g., COUNT BY class_name) while
supporting any future annotation type.
```
### Table 3.1: Core Database Schema (Initial)

This table outlines the foundational tables for the application. All tables _must_ be created


within the public schema and include a workspace_id column (or a path to one) to enforce
RLS.

```
Table Column Type Notes
```
```
workspaces id uuid PK. Represents the
Tenant.
```
```
name text
```
```
users id uuid PK. Foreign key to
auth.users(id).^19
```
(^) email text
workspace_membe
rs
id uuid PK.
user_id uuid FK to users(id)
workspace_id uuid FK to
workspaces(id)
role text admin, member
(Workspace-level
role)
projects id uuid PK.
workspace_id uuid FK to
workspaces(id).
**RLS key.**
name text
project_type text object_detection,
segmentation,
keypoint, etc. 105


```
images id uuid PK.
```
```
project_id uuid FK to projects(id).
RLS key.
```
```
storage_path text Path to the file in
S3/R2.^106
```
(^) filename text
width integer
height integer
annotations id uuid PK.
image_id uuid FK to images(id).
**RLS key.**
project_id uuid FK to projects(id).
**Indexed.**
class_name text **Indexed.** For fast
analytics.
annotator_id uuid FK to users(id).
data jsonb The annotation
payload (e.g.,
{"box": [x,y,w,h]}).^101
(^) status text draft, submitted,
approved (for
review workflow) 63

### 3.2. Core Identity, Tenancy & RBAC


```
● Identity (AuthN): Handled entirely by Supabase Auth.^19 The FastAPI backend will not
have register or login endpoints. Client authentication is handled by the Next.js app using
@supabase/ssr.^12
● Tenancy (RLS):
○ The entire platform is multi-tenant.^44 The workspaces table represents the "Tenant."
All core resource tables (projects, images, annotations, etc.) must have a
workspace_id (or be joinable to a table that does) to serve as the RLS key.^44
○ Mandated RLS Policy: RLS must be enabled on all tables. A base policy will be:
SQL
-- This helper function gets the tenant_id from the user's JWT custom claim [10, 43]
CREATE FUNCTION auth.tenant_id() RETURNS uuid AS $$
SELECT (auth.jwt() ->> 'tenant_id')::uuid;
$$ LANGUAGE sql STABLE;
```
```
-- Example RLS Policy for 'projects' table
CREATE POLICY "User can see their own workspace projects"
ON public.projects FOR SELECT
USING ( workspace_id = auth.tenant_id() );
```
```
● Authorization (RBAC):
○ This is distinct from RLS. RLS answers "Can you see this row ?" RBAC answers "Can
you perform this action ?".^11
○ RBAC will be implemented for project-level roles 45 via a new table:
project_members (id, project_id, user_id, role text)
○ The role will be admin, reviewer, or labeler.^45
○ FastAPI endpoints will use a dependency-injected "authorizer" that checks this role
(e.g., @Depends(RoleRequired("reviewer"))).
```
### 3.3. API Authentication (FastAPI + Supabase JWT)

```
● Directive: The FastAPI backend must validate Supabase JWTs locally for performance
and resilience. Calling auth.get_user() on every API request is an anti-pattern that
introduces unacceptable latency and a network dependency.^16
● Implementation (auth_dependency.py):
```
1. The Supabase JWT_SECRET 19 will be stored as an environment variable
    (SUPABASE_JWT_SECRET) in the apps/api service.
2. A FastAPI HTTPBearer dependency will be created.^16
3. This dependency will:
    a. Extract the token from the Authorization: Bearer header.


```
b. Use python-jwt 110 to decode the token: jwt.decode(token,
SETTINGS.supabase_jwt_secret, audience="authenticated", algorithms=).
c. On failure (expired, invalid), it raises a HTTPException(401).
d. On success, it extracts the sub (user_id) and custom tenant_id claims.
e. It returns a Pydantic model AuthenticatedUser(id: uuid, tenant_id: uuid).
```
4. All protected endpoints will use this dependency: async def get_project(user:
    AuthenticatedUser = Depends(get_current_user)).^16

### 3.4. Frontend (Next.js) Shell & Auth

```
● Directive: The apps/web project will be initialized as a Next.js 15 App Router
application.^12
● Authentication: The @supabase/ssr package must be used.^13 This is the official library
for handling Supabase auth in an SSR environment.
● Implementation:
```
1. Create utils/supabase/client.ts (for Client Components) and utils/supabase/server.ts
    (for Server Components, Server Actions, and Route Handlers) as per the Supabase
    documentation.^13
2. Implement middleware.ts to manage the user's session and refresh the token on
    each request.^13
3. Create a (auth) route group for login, register, and auth-callback pages.
4. Create a (app) route group for the main, authenticated application layout. This layout
    will use the server.ts client to fetch the user. If no user exists, it will redirect() to /login.
    This protects all app routes.^112

### 3.5. Enterprise SSO (SAML)

```
● Directive: To satisfy enterprise requirements, the platform must support SAML 2.0.^75
● Implementation: This is a P1 feature. Supabase Auth supports SAML 2.0.^75 The
implementation will involve:
```
1. Building a settings UI for Workspace Admins to configure their SAML Identity
    Provider (IdP) metadata (e.g., Okta 113 ).
2. This UI will call the Supabase Admin API to register the IdP.
3. The login page will dynamically show a "Login with SSO" button if an SSO email is
    entered.


## Part 4: Phase 3 - Data Ingestion & Storage

### 4.1. Storage Architecture (Decoupled S3/R2)

```
● Directive: As established in Part 1, this platform will not use Supabase Storage as the
primary media store. A dedicated, S3-compatible object store (e.g., Cloudflare R2 for
cost savings on egress 114 , or AWS S3) will be used.
● This decoupling is critical for enterprise scale. The database (images table) only stores
metadata and a storage_path.^106 This allows storage and the database to be scaled
independently and, crucially, keeps high-bandwidth file transfers off the API servers.^14
```
### 4.2. Secure Upload Pipeline (Presigned URLs)

```
● User Stories:
○ "As an annotator, I want to drag and drop a folder of 10,000 images onto the browser
to upload them to my project."
○ "As a security admin, I must ensure that the client (browser) never has access to
persistent S3 credentials."
● Mandated Flow: The only secure pattern to achieve this is by using presigned URLs.^14
```
1. **Client Request:** The Next.js client (apps/web) iterates through the user's selected
    files. For each file, it makes a POST request to our backend: POST
    /api/v1/projects/{project_id}/upload_url with a JSON body: { "filename": "image1.jpg",
    "content_type": "image/jpeg" }.
2. **API Authorization:** The FastAPI backend (apps/api) receives this. It uses the auth
    dependency (Part 3.3) to get the user and tenant_id. It verifies that this user has
    write access to this project_id.
3. **API URL Generation:** The API, using the boto3 (or equivalent S3) SDK, generates a
    **presigned POST URL** 17 valid for a single file upload, scoped to a specific S3 key
    (e.g., s3://<bucket_name>/<tenant_id>/<project_id>/image1.jpg) and a short expiry
    (e.g., 5 minutes).
4. **API Response:** The API returns the presigned_url and the storage_path to the client.
5. **Client Upload:** The Next.js client receives this URL and performs a PUT (or POST)
    request _directly to S3/R2_ with the file data.^14 This bypasses our API server entirely 14 ,


```
a critical scaling optimization.
```
6. **Client Confirmation:** On successful upload (HTTP 200 from S3), the client sends a
    _final_ confirmation to our backend: POST /api/v1/images/complete_upload with {
    "storage_path": "...", "width": 1920, "height": 1080 }.
7. **API Confirmation:** The API receives this, validates the path, and _only then_ writes the
    final record to the public.images table in Postgres.

### 4.3. Programmatic Upload API (Active Learning)

```
● Directive: To enable active learning loops 51 , the platform must provide a programmatic
upload API.^5 This is a P1 feature.
● Implementation:
○ This API will not use presigned URLs, as it is a server-to-server interaction.
○ Define a new API router: POST /api/v1/projects/{project_id}/upload_image.^119
○ This endpoint will take an UploadFile 116 and an API key.
○ The API key will be a scoped API key 5 generated by the user, not their Supabase
JWT.
○ The FastAPI endpoint will stream the file directly from the request body to the S
bucket 116 and then create the images table record.
```
### 4.4. Third-Party Integrations (Import)

```
● Directive: Users must be able to import existing datasets.^7
● Implementation:
○ P1 - S3 Bucket Import: A UI where a user provides AWS credentials and an S
bucket path.^7 An ARQ worker 9 will be enqueued to scan this bucket and create
images records for each file found.
○ P2 - Format Import: A UI to upload zip files containing images and annotation files
(e.g., CVAT XML, LabelMe JSON, VoTT).^7 An ARQ worker will parse these files, ingest
the images, and create the corresponding annotations records in our database.
```
## Part 5: Phase 4 - The Annotation Workbench


### 5.1. Workbench Architecture (Next.js + Canvas)

```
● Directive: The annotation interface must be high-performance, responsive, and capable
of handling complex interactions. A standard DOM-based (HTML/CSS) tool is not
acceptable for this task; a canvas-based library is required.^121
● Mandated Libraries:
○ 2D Annotation: Konva.js.^122 It is used by competitors (e.g., Labelbox 122 ) and is known
to be high-performance, unlike Fabric.js which has been reported as slow with many
objects.^123
○ 3D Annotation: Three.js.^124 This is the industry standard for WebGL-based 3D
rendering and is explicitly used for LiDAR visualization.^126
○ Temporal Annotation: A React-Timeline component (e.g., Planby 127 or a
custom-built solution based on the principles of 143 ). This will be used for temporal
video annotation.^73
```
### 5.2. Collaborative Annotation Engine (Supabase Realtime)

```
● User Story: "As a QA Reviewer, I want to join an annotation session with a trainee, see
their cursor and annotations in real-time, and leave comments 128 on their work without a
page refresh."
● Differentiator: Roboflow supports collaboration 129 , but a live, real-time experience is a
significant differentiator. The mandated stack includes Supabase, which provides
Supabase Realtime.^20 Realtime's three key features— Broadcast , Presence , and
Postgres Changes 20 —map perfectly to a Figma-like 132 collaborative tool.^133
● Mandated Flow:
```
1. **Joining:** A user opens an image. The Next.js client joins a Supabase Realtime
    channel for that image (e.g., channel = supabase.channel('image:uuid-12345')).
2. **Presence (Who's Online):** The client calls channel.track({ user: 'name', cursor: {x:0,
    y:0} }). All other users on the channel receive "presence-diff" events and can render
    the user's avatar and cursor.^133
3. **Broadcast (Live Data):** When the user draws a new annotation (e.g.,
    on_mouse_move), the client _broadcasts_ a lightweight JSON payload of the
    in-progress annotation 135 via channel.send(). This data is _not_ saved to the DB; it is
    ephemeral. Other clients receive this and render a "ghost" annotation.
4. **Postgres Changes (Saved Data):** When the user _saves_ the annotation, the client
    makes a standard API call (POST /api/v1/annotations). The API writes to the


```
annotations table. The Supabase "Postgres Changes" feature 20 (which will be
enabled on the annotations table) automatically sends the final, saved annotation
data to all clients on the channel, who then replace the "ghost" annotation with the
permanent one.
```
### 5.3. Annotation Tooling (User Stories & Implementation)

```
● P0 - Object Detection (Bounding Box) 137 :
○ User Story: "As an annotator, I want to click and drag to draw a tight bounding box 137
around an object and assign it a class."
○ Implementation: Use Konva.js Rect shapes. Implement hotkeys (B) 53 and class
selection modals.
● P0 - Classification (Full-image) 52 :
○ User Story: "As an annotator, I want to assign one or more classes (multi-label) to an
entire image."
○ Implementation: This is a UI-only feature. The annotations table will store this with a
data payload like {"type": "classification", "classes": ["daytime", "cloudy"]}.
● P1 - Segmentation (Polygon) 53 :
○ User Story: "As an annotator, I want to click points around an object to create a
pixel-perfect polygon mask."
○ Implementation: Use Konva.js Line and Shape components. Must support
adding/deleting vertices.
● P1 - Smart Polygon (SAM) 138 :
○ User Story: "As an annotator, I want to click on an object, and have the 'Smart
Polygon' tool 138 (powered by Segment Anything Model) automatically generate a
tight polygon mask for me."
○ Implementation: This requires an ML model (SAM). The client will send the image and
a (x,y) click coordinate to a dedicated FastAPI inference endpoint 61 (or run SAM
in-browser 139 ). The endpoint returns the polygon, which is then loaded into the
Konva.js canvas.
● P1 - Keypoint Detection 140 :
○ User Story: "As a project admin, I want to define a 'skeleton' (e.g., 'human_pose' with
'head', 'shoulder_l', 'shoulder_r').^141 As an annotator, I want to place these keypoints
on an image and mark them as visible or occluded.^140 "
○ Implementation: A new DB table keypoint_skeletons is required. The UI will first draw
a bounding box 140 , then display the defined skeleton points within it for the
annotator to position.
```

### 5.4. Advanced Data Types ("And Then Some")

```
● P2 - Temporal Video Annotation 73 :
○ User Story: "As an annotator, I want to label actions in a video, (e.g., 'person_running'
from 0:05.1s to 0:08.3s) and track objects across frames."
○ Implementation: This requires a new UI component: a multi-track timeline.^127 The
annotator will label a temporal segment. The system must also support interpolation ,
where an annotator labels a bounding box on frame 1 and frame 10, and the system
auto-generates the boxes for frames 2-9.
● P2 - 3D Point Cloud/LiDAR Annotation 71 :
○ User Story: "As an autonomous vehicle researcher, I want to upload a .pcd / .las file,
view it in a 3D space, and draw 3D bounding boxes (cuboids) around cars and
pedestrians."
○ Implementation: This is a major feature. It requires Three.js 124 to render the point
cloud. The UI must support 3D navigation (pan, orbit, zoom) and drawing 3D cuboids,
not 2D boxes.^145
```
## Part 6: Phase 5 - Data Versioning & Transformation

### 6.1. Dataset Versioning Engine

```
● User Story: "As an ML engineer, my source dataset has 10,000 images. I want to create
a new, versioned dataset 55 that is preprocessed (all images resized to 640x640) 23 and
augmented (3x, with random flips and brightness changes).^22 I must be able to track this
version and reproduce it later."
● This is the core of the MLOps loop. The "Generate New Version" button 55 is the trigger
for our ARQ task queue.
```
### 6.2. Asynchronous Task Queue (ARQ)


```
● Directive: All dataset generation must be handled by the ARQ worker service
(apps/workers).
● Workflow:
```
1. A standard API request 15 is synchronous and will time out.
2. Celery is a complex dependency. ARQ is asyncio-native, lightweight, and a perfect fit
    for FastAPI.^9
3. Therefore, the "Generate" button's API endpoint (POST
    /api/v1/projects/{id}/generate_version) will only do two things:
    a. Create a new row in a dataset_versions table with status: "QUEUED" and the jsonb
    config for preprocessing/augmentations.
    b. Enqueue an ARQ job: await redis.enqueue_job('generate_version_task', version_id)
    c. Return an HTTP 202 Accepted to the client immediately.
4. The ARQ worker (a separate compute process) will pick up this job, perform the
    CPU-heavy image processing 22 , and update the dataset_versions row to status:
    "COMPLETED" upon finishing.

### 6.3. Preprocessing Pipeline

23

```
● Directive: The ARQ worker must support all baseline preprocessing steps. These apply
to all splits (train/valid/test).^23
● Implementation: A preprocessing module will be built using OpenCV-Python or
albumentations.^56
● P0 Features: Auto-Orient, Resize (Stretch, Fit, Pad), Grayscale, Auto-Adjust Contrast.
● P1 Features: Isolate Objects, Static Crop, Tile, Modify Classes, Filter Null.
```
### 6.4. Augmentation Pipeline

22

```
● Directive: The ARQ worker must support all baseline augmentation steps. These apply
only to the training split.^22
● Implementation: The albumentations library 56 is mandated as it is the industry standard
and supports transformations for bounding boxes, masks, and keypoints simultaneously.
● P0 Features: Flip (Horizontal, Vertical), Rotate, Crop.
● P1 Features: Shear, Hue/Saturation/Brightness, Blur, Noise, Cutout.
● The UI must allow the user to select how many augmented versions to create (e.g.,
```

```
"3x").^22 The worker will de-duplicate any identical images created during this random
process.^22
```
### 6.5. Universal Export

24

```
● User Story: "As an ML engineer, I've generated my 'v3-augmented' dataset. I now want to
export it in 'YOLOv8 PyTorch TXT' 57 format to train in my own environment."
● Implementation: This is another ARQ task.
```
1. User clicks "Export" and selects a format.^57
2. API enqueues an export_task.
3. ARQ worker reads the dataset_versions manifest, formats the annotations into the
    desired format (e.g., COCO JSON 24 , PASCAL VOC XML 148 ), zips the result, and saves
    it to S3/R2.
4. The UI provides a download link when the task is complete.

## Part 7: Phase 6 - MLOps: Training & Deployment

### 7.1. Model Training Service (Orchestration)

```
● User Story: "As a project manager, I have a 'v3-augmented' dataset. I want to select
'Train Model', choose the 'YOLOv11' 58 architecture, and receive a trained model file and
performance metrics (mAP, precision, recall) 1 without writing any code."
● Architectural Mandate: Training is a long-running, GPU-intensive, complex, and
failure-prone process. It must be run in a separate, managed compute environment.
Kubernetes is the standard.^149
● Kubeflow 8 provides "Training Operators" 25 that manage the lifecycle of distributed
training jobs (e.g., PyTorchJob, XGBoostJob).
● Our FastAPI backend's role is Orchestrator , not Executor. The API must not execute
training directly.
● Mandated Flow:
```
1. A Kubernetes cluster with Kubeflow installed is a prerequisite for this feature.
2. User clicks "Train".^58


3. FastAPI API (POST /api/v1/versions/{id}/train):
    a. Creates a models table row with status: "PENDING".
    b. Generates a PyTorchJob (or similar) YAML manifest. This manifest instructs
    Kubeflow to:
    i. Spin up a new pod with a trainer image (e.g., visionflow/yolov8-trainer:latest).
    ii. Mount the dataset v3-augmented (as a zip/manifest) from S3/R2.
    iii. Pass hyperparameters as environment variables.
    c. FastAPI applies this manifest to the K8s API.
4. ARQ Worker (or a K8s controller): A separate process monitors the status of the
    PyTorchJob CRD in Kubernetes.
5. When the job finishes, the worker pulls the metrics (mAP, etc.) and the final model
    weights (.pt file) from the job's output (saved to S3/R2) and updates the models table
    row (status: "COMPLETED").

### 7.2. Model-Assisted Labeling (Active Learning Loop)

```
● User Story: "As an annotator, I have 1,000 new, unlabeled images. I want to use my 'v3'
model to pre-label all of them so I only have to review and correct the annotations, not
create them from scratch.^52 "
● Implementation (Label Assist) 62 :
```
1. A UI in the annotation workbench allows the user to select one of their trained
    models (or a public one 62 ).
2. When an image is opened, the client sends the image to the model's inference API
    (see 7.3).
3. The API returns a list of predicted annotations (boxes, polygons).
4. The Konva.js canvas renders these as "suggested" annotations, which the user can
    accept, reject, or modify.
5. This creates the "human-in-the-loop" workflow.^137
● "And Then Some" (Advanced Active Learning) 67 :
○ This is a P2 feature and a key differentiator.
○ Instead of just pre-labeling, an active learning pipeline will be built to find the _most
valuable_ images to label.
○ **P1 - Confidence-Based:** Provide an "Upload API" 51 and document how users can
send back images where model confidence is low.^67
○ **P2 - Diversity-Based:** Implement a pipeline 69 that runs inference on 100,000
unlabeled images, extracts embeddings, clusters them, and samples images from
under-represented clusters. This finds "novel" data the model has never seen.
○ **P2 - Category-Aware:** Implement strategies to sample more images from minority
classes to fix class imbalance.^70


### 7.3. Hosted Inference Service

```
● User Story: "As a developer, I have a trained model 'v3'. I want a secure, scalable REST
API endpoint 59 that I can send new images to and get predictions back in JSON format."
● Implementation:
○ This will be a new FastAPI-based service: the Inference Gateway.^61
○ When a user "deploys" a model, our backend provisions a new endpoint on this
gateway.
○ For serverless, low-traffic needs, this can be a KServe 8 service on Kubernetes that
scales to zero.
○ The gateway will handle request authentication (using scoped API keys), load the
model weights from S3, run inference (on a GPU-enabled pod), and return the JSON
response.^59
```
## Part 8: Phase 7 - Enterprise Collaboration &

## Governance

### 8.1. Team Management & Roles

```
● Directive: Implement project-level RBAC.^45
● Implementation:
○ The project_members table (from Part 3.2) is the source of truth.
○ Admin: Full CRUD on the project. Can invite users, start training, delete.
○ Reviewer: Can assign tasks, annotate, and approve/reject submitted annotations.^45
○ Labeler: Can only work on tasks assigned to them.^45 They can annotate and submit
for review, but cannot approve.
● Table 8.1: RBAC Permission Matrix: A detailed matrix (to be built) will map every API
endpoint (e.g., DELETE /projects/{id}) to the required role.
```
### 8.2. Annotation Workflow Management


```
● User Story: "As a project manager, I want to select 500 images, assign them to my three
labelers 52 , monitor their progress in an 'at-a-glance' view 52 , and then review all their
submitted work in a single queue.^156 "
● Superior Workflow: This feature will be built on a new table: annotation_tasks (id,
project_id, image_id, job_id, assignee_id, status, reviewer_id).
```
1. The "Assign" UI creates records in this table.
2. The "Labeler" queue is a simple SELECT... WHERE assignee_id = current_user AND
    status = 'PENDING'.
3. The "Reviewer" queue is a SELECT... WHERE project_id = X AND status =
    'SUBMITTED'.
4. This is a robust, auditable, and scalable system that is far superior to Roboflow's
    documented "merge datasets" workaround.^64

### 8.3. Collaboration Tools

```
● User Story: "As a reviewer, I am rejecting an annotation. I want to drop a pin on the
image, add a comment 128 , and @-mention 157 the original labeler to tell them why it's
wrong."
● Implementation:
○ A new table: image_comments (id, image_id, user_id, position_x, position_y,
comment_text).
○ The annotation workbench will have a "Comment" tool.^128
○ The comment_text will be parsed for @mentions to send in-app notifications (which
can be powered by Supabase Realtime 20 ).
```
### 8.4. Annotation Analytics

```
● User Story: "As a manager, I want a dashboard to see the health of my dataset (class
balance, annotation heatmap) 1 and the performance of my team (time spent,
annotations per person, approval rate).^52 "
● Implementation:
○ This is a P2 feature that is now easy to build.
○ The "Dataset Health" dashboard 1 is a series of SQL queries against the annotations
table (GROUP BY class_name).
○ The "Team Performance" dashboard 66 is a series of SQL queries against the
```

```
annotation_tasks table (GROUP BY assignee_id, status).
```
## Part 9: Phase 8 - Production Deployment & Launch

### 9.1. Production Architecture

```
● Web App: The apps/web Next.js application will be deployed to Vercel. Vercel's deep
integration with Next.js provides the best performance (SSR, edge routing) and CI/CD.^158
● API & Services: The apps/api (FastAPI), apps/workers (ARQ), and all ML services
(Kubeflow, Inference Gateway) will be containerized and deployed to a Kubernetes
Cluster (e.g., EKS, GKE).^149
● Database: A production-tier Supabase Cloud instance 3 will be used for high availability,
PITR, and managed services.
● Storage: Cloudflare R2 or AWS S3 for object storage.^27
```
### 9.2. Database Scaling (Pgbouncer)

```
● Problem: A high-concurrency FastAPI app 15 and Vercel's serverless functions will create
a massive number of database connections, easily exhausting the Postgres limit.^89
● Mandate (Non-Negotiable): The production apps/api and apps/workers services must
connect to the Supabase Cloud database using the Transaction-mode Connection
Pooler (Pgbouncer).^18
● Implementation: The database connection string in the production environment
variables must point to the pgbouncer port (6543), not the direct Postgres port (5432). All
local development (Part 2.3) and CI testing (Part 2.4) must also use Pgbouncer to detect
any transaction-pooling-related errors 90 before they hit production.
```
### 9.3. Finalized CI/CD Pipelines

```
● Directive: The CI/CD pipeline in GitHub Actions 93 will be expanded for production
```

```
deployment.
● Implementation:
```
1. **On push to main (Deploy to Staging):**
    ■ Lint, Test, Build (as in 2.4).
    ■ Build and push api and workers Docker images to a container registry (e.g., ECR).
    ■ Deploy updated images to the _Staging_ Kubernetes cluster.
    ■ Trigger a Vercel deployment for the apps/web frontend, pointing to the _Staging_
       API.
    ■ Run the E2E test suite (9.4) against the staging environment.
2. **On release (Deploy to Production):**
    ■ A manual-trigger-only workflow.
    ■ Promotes the _exact Docker images_ and Vercel build from Staging to the
       Production environment. This ensures what was tested is what is deployed.

### 9.4. End-to-End Testing (Playwright)

```
● Directive: Unit tests are insufficient for the Annotation Workbench. The platform's most
complex logic is the user interaction with the canvas.
● Mandate: A comprehensive E2E test suite must be built using Playwright.^159 Cypress 159
is not acceptable, as Playwright offers superior cross-browser testing and native
async/await.
● Implementation:
○ A new package, /apps/e2e-tests, will be created.
○ Test cases must cover the full user journey:
```
1. test_signup_and_create_project.spec.ts
2. test_upload_image.spec.ts (Must mock the S3 presigned URL flow).
3. test_annotation_bounding_box.spec.ts: This test must programmatically load an
    image, select the 'box' tool, draw a box on the Konva.js canvas, and verify that
    the correct annotation is created and saved.
4. test_workflow_submit_and_approve.spec.ts: Must log in as a Labeler, submit an
    annotation, log out, log in as a Reviewer, and approve the annotation.
5. test_collaboration_realtime.spec.ts: Must launch two browser contexts (User A,
    User B), have both open the same image, and verify that User B can see User A's
    cursor and "ghost" annotations via Supabase Realtime.

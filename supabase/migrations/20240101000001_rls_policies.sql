-- Row-Level Security (RLS) Policies
-- This implements database-level multi-tenancy as mandated in the PRD

-- Helper function to get tenant_id from JWT
CREATE OR REPLACE FUNCTION auth.tenant_id()
RETURNS UUID AS $$
    SELECT COALESCE(
        (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::UUID,
        (auth.jwt() ->> 'tenant_id')::UUID
    );
$$ LANGUAGE SQL STABLE;

-- Helper function to get user_id from JWT
CREATE OR REPLACE FUNCTION auth.user_id()
RETURNS UUID AS $$
    SELECT (auth.jwt() ->> 'sub')::UUID;
$$ LANGUAGE SQL STABLE;

-- Enable RLS on all tables
ALTER TABLE public.workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workspace_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.project_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.images ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.annotations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dataset_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.annotation_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.image_comments ENABLE ROW LEVEL SECURITY;

-- Workspaces: Users can see workspaces they are members of
CREATE POLICY "Users can view their workspaces"
    ON public.workspaces FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.workspace_members
            WHERE workspace_members.workspace_id = workspaces.id
            AND workspace_members.user_id = auth.user_id()
        )
    );

CREATE POLICY "Workspace admins can insert workspaces"
    ON public.workspaces FOR INSERT
    WITH CHECK (true);  -- Users can create workspaces

CREATE POLICY "Workspace admins can update their workspaces"
    ON public.workspaces FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM public.workspace_members
            WHERE workspace_members.workspace_id = workspaces.id
            AND workspace_members.user_id = auth.user_id()
            AND workspace_members.role = 'admin'
        )
    );

-- Users: Users can view their own record
CREATE POLICY "Users can view their own record"
    ON public.users FOR SELECT
    USING (id = auth.user_id());

CREATE POLICY "Users can insert their own record"
    ON public.users FOR INSERT
    WITH CHECK (id = auth.user_id());

-- Workspace Members: Users can view members of their workspaces
CREATE POLICY "Users can view workspace members"
    ON public.workspace_members FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.workspace_members wm
            WHERE wm.workspace_id = workspace_members.workspace_id
            AND wm.user_id = auth.user_id()
        )
    );

CREATE POLICY "Workspace admins can manage members"
    ON public.workspace_members FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM public.workspace_members
            WHERE workspace_members.workspace_id = workspace_members.workspace_id
            AND workspace_members.user_id = auth.user_id()
            AND workspace_members.role = 'admin'
        )
    );

-- Projects: Users can see projects in their workspaces
CREATE POLICY "Users can view projects in their workspace"
    ON public.projects FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.workspace_members
            WHERE workspace_members.workspace_id = projects.workspace_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

CREATE POLICY "Workspace members can create projects"
    ON public.projects FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.workspace_members
            WHERE workspace_members.workspace_id = projects.workspace_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

-- Project Members: Users can view members of projects they have access to
CREATE POLICY "Users can view project members"
    ON public.project_members FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.projects
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE projects.id = project_members.project_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

-- Images: Users can view images in projects they have access to
CREATE POLICY "Users can view images in their projects"
    ON public.images FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.projects
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE projects.id = images.project_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

CREATE POLICY "Project members can insert images"
    ON public.images FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.projects
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE projects.id = images.project_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

-- Annotations: Users can view annotations in projects they have access to
CREATE POLICY "Users can view annotations in their projects"
    ON public.annotations FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.projects
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE projects.id = annotations.project_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

CREATE POLICY "Project members can create annotations"
    ON public.annotations FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.projects
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE projects.id = annotations.project_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

CREATE POLICY "Annotators can update their own annotations"
    ON public.annotations FOR UPDATE
    USING (annotator_id = auth.user_id());

CREATE POLICY "Annotators can delete their own annotations"
    ON public.annotations FOR DELETE
    USING (annotator_id = auth.user_id());

-- Dataset Versions: Users can view versions in their projects
CREATE POLICY "Users can view dataset versions"
    ON public.dataset_versions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.projects
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE projects.id = dataset_versions.project_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

-- Annotation Tasks: Users can view tasks in their projects
CREATE POLICY "Users can view annotation tasks"
    ON public.annotation_tasks FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.projects
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE projects.id = annotation_tasks.project_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

-- Image Comments: Users can view comments on images they have access to
CREATE POLICY "Users can view image comments"
    ON public.image_comments FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.images
            JOIN public.projects ON projects.id = images.project_id
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE images.id = image_comments.image_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

CREATE POLICY "Users can create image comments"
    ON public.image_comments FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.images
            JOIN public.projects ON projects.id = images.project_id
            JOIN public.workspace_members ON workspace_members.workspace_id = projects.workspace_id
            WHERE images.id = image_comments.image_id
            AND workspace_members.user_id = auth.user_id()
        )
    );

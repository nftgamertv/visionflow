/**
 * Core TypeScript types used across the frontend.
 * These complement the auto-generated Zod schemas.
 */

export type ProjectType =
  | 'object_detection'
  | 'segmentation'
  | 'classification'
  | 'keypoint'

export type AnnotationStatus = 'draft' | 'submitted' | 'approved'

export type UserRole = 'admin' | 'reviewer' | 'labeler'

export type AnnotationType =
  | 'bounding_box'
  | 'polygon'
  | 'keypoint'
  | 'classification'
  | '3d_cuboid'

export interface BoundingBoxData {
  type: 'bounding_box'
  x: number
  y: number
  width: number
  height: number
}

export interface PolygonData {
  type: 'polygon'
  points: Array<{ x: number; y: number }>
}

export interface KeypointData {
  type: 'keypoint'
  points: Array<{
    x: number
    y: number
    visible: boolean
    label: string
  }>
}

export interface ClassificationData {
  type: 'classification'
  classes: string[]
}

export type AnnotationData =
  | BoundingBoxData
  | PolygonData
  | KeypointData
  | ClassificationData

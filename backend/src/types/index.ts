// Document related types
export interface Document {
  id: string
  fileName: string
  fileUrl: string
  uploadedAt: Date
  status: 'pending' | 'analyzing' | 'completed' | 'failed'
  mimeType: string
  size: number
}

export interface ComplianceIssue {
  id: string
  severity: 'high' | 'medium' | 'low'
  category: string
  description: string
  confidenceScore: number
  location?: string
  recommendation?: string
}

export interface ComplianceReport {
  id: string
  documentId: string
  documentName: string
  analysisDate: Date
  issues: ComplianceIssue[]
  overallRiskScore: number
  summary: string
  processingTimeMs: number
}

export interface GenAIRequest {
  text: string
  documentType?: string
}

export interface GenAIResponse {
  issues: ComplianceIssue[]
  summary: string
  riskScore: number
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

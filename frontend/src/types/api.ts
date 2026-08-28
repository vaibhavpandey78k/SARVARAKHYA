export type ReportType = 'UA' | 'UC' | 'Near Miss' | 'Incident' | null;
export type Confidence = 'High' | 'Medium' | 'Low' | string;
export type ReviewStatus = 'Pending' | 'Reviewed' | 'Requires Review' | string;

export interface CreateReportRequest { report_text: string; report_type: ReportType; site: string | null; date: string | null; }
export interface CreateReportResponse { id: string; report_text: string; report_type: string | null; site: string | null; date: string | null; created_at: string; }

export interface Analysis {
  sif_prediction: boolean | null;
  sif_probability: number;
  analysis_type?: string;
  model_version?: string;
  sif_status?: string;
  sif_score?: number | null;
  confidence: Confidence;
  life_saving_rules: string[];
  activity: string;
  location: string;
  barrier_failure: string;
  evidence: string[];
  review_status: ReviewStatus;
  reviewer_correction?: boolean | null;
}
export interface AnalyzeResponse extends Analysis { report_id: string; }
export interface Report { id: string; report_text: string; report_type: string | null; site: string | null; date: string | null; analysis?: Analysis | null; created_at?: string; }

export interface DashboardOverview { total_reports: number; sif_reports: number; sif_percentage: number; critical_precursors: number; }
export interface SiteRisk { site: string; report_count: number; sif_count: number; sif_density: number; }
export interface ActivityRisk { activity: string; report_count: number; sif_count: number; sif_density: number; }
export interface RuleDistribution { rule: string; count: number; percentage: number; }
export interface Precursor { id: string; activity: string; location: string; barrier_failure: string; occurrence_count: number; sif_count: number; sif_density: number; trend_percentage: number; affected_sites: string[]; }
export interface ItemResponse<T> { items: T[]; }

export interface ReportsListQuery { search?: string; sif?: 'all' | 'sif' | 'non-sif'; site?: string; activity?: string; rule?: string; minConfidence?: string; date?: string; page?: number; pageSize?: number; }
export interface ReportsListResponse { items: Report[]; total: number; page: number; page_size: number; }

export interface ApiClient {
  createReport(payload: CreateReportRequest): Promise<CreateReportResponse>;
  analyzeReport(id: string): Promise<AnalyzeResponse>;
  getReport(id: string): Promise<Report>;
  listReports(query?: ReportsListQuery): Promise<ReportsListResponse>;
  getDashboardOverview(): Promise<DashboardOverview>;
  getDashboardSites(): Promise<ItemResponse<SiteRisk>>;
  getDashboardActivities(): Promise<ItemResponse<ActivityRisk>>;
  getDashboardRules(): Promise<ItemResponse<RuleDistribution>>;
  getDashboardPrecursors(): Promise<ItemResponse<Precursor>>;
}

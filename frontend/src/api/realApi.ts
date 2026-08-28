import type { ApiClient, AnalyzeResponse, CreateReportRequest, CreateReportResponse, DashboardOverview, ItemResponse, Precursor, Report, ReportsListQuery, ReportsListResponse, RuleDistribution, SiteRisk, ActivityRisk, Analysis } from '../types/api';

type BackendPrediction = {
  id: string; report_id: string; analysis_type: string; model_version: string;
  sif_prediction: boolean | null; sif_status: string; sif_score: number | null;
  sif_probability: number | null; confidence: string; life_saving_rules: string[];
  activity: string | null; location: string | null; barrier_failure: string | null;
  evidence: string[]; review_status?: string; reviewer_correction?: boolean | null; created_at: string;
};
type BackendReport = {
  id: string; source_id: string | null; event_date: string | null; employer: string | null;
  city: string | null; state: string | null; source?: string | null; final_narrative: string;
  created_at: string; predictions: BackendPrediction[];
};

const REPORT_TYPES = new Set(['UA', 'UC', 'Near Miss', 'Incident']);

function normalizeAnalysis(p?: BackendPrediction | null): Analysis | null {
  if (!p) return null;
  return {
    sif_prediction: p.sif_prediction,
    sif_probability: p.sif_probability ?? p.sif_score ?? 0,
    confidence: p.confidence,
    life_saving_rules: p.life_saving_rules || [],
    activity: p.activity || '',
    location: p.location || '',
    barrier_failure: p.barrier_failure || '',
    evidence: p.evidence || [],
    review_status: p.review_status || 'Pending',
    reviewer_correction: p.reviewer_correction ?? null,
    analysis_type: p.analysis_type,
    model_version: p.model_version,
    sif_status: p.sif_status,
    sif_score: p.sif_score,
  };
}

function normalizeReport(r: BackendReport): Report {
  const latest = [...(r.predictions || [])].sort((a, b) => b.created_at.localeCompare(a.created_at))[0];
  return {
    id: r.id,
    report_text: r.final_narrative,
    report_type: r.source && REPORT_TYPES.has(r.source) ? r.source : null,
    site: r.employer,
    date: r.event_date,
    analysis: normalizeAnalysis(latest),
    created_at: r.created_at,
  };
}

export class RealApi implements ApiClient {
  private base = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');
  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await fetch(`${this.base}${path}`, { headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) }, ...init });
    if (!res.ok) {
      let message = `Backend request failed (${res.status})`;
      try { const body = await res.json(); message = body.detail || message; } catch { /* keep status message */ }
      throw new Error(message);
    }
    return res.json() as Promise<T>;
  }

  async createReport(payload: CreateReportRequest): Promise<CreateReportResponse> {
    const body = {
      report_text: payload.report_text,
      report_type: payload.report_type,
      site: payload.site,
      event_date: payload.date || null,
    };
    const r = await this.request<BackendReport>('/api/reports', { method: 'POST', body: JSON.stringify(body) });
    return { id: r.id, report_text: r.final_narrative, report_type: r.source && REPORT_TYPES.has(r.source) ? r.source : null, site: r.employer, date: r.event_date, created_at: r.created_at };
  }

  async analyzeReport(id: string): Promise<AnalyzeResponse> {
    const p = await this.request<BackendPrediction>(`/api/reports/${encodeURIComponent(id)}/analyze`, { method: 'POST' });
    return { ...normalizeAnalysis(p)!, report_id: p.report_id };
  }

  async getReport(id: string): Promise<Report> {
    const r = await this.request<BackendReport>(`/api/reports/${encodeURIComponent(id)}`);
    return normalizeReport(r);
  }

  async listReports(query: ReportsListQuery = {}): Promise<ReportsListResponse> {
    const params = new URLSearchParams();
    if (query.search) params.set('search', query.search);
    if (query.sif && query.sif !== 'all') params.set('sif', query.sif);
    if (query.site) params.set('site', query.site);
    if (query.activity) params.set('activity', query.activity);
    if (query.rule) params.set('rule', query.rule);
    if (query.minConfidence) params.set('minConfidence', query.minConfidence);
    if (query.date) params.set('date', query.date);
    params.set('page', String(query.page || 1));
    params.set('pageSize', String(query.pageSize || 5));
    const data = await this.request<{items: BackendReport[]; total: number; page: number; page_size: number}>(`/api/reports?${params}`);
    return { items: data.items.map(normalizeReport), total: data.total, page: data.page, page_size: data.page_size };
  }

  getDashboardOverview() { return this.request<DashboardOverview>('/api/dashboard/overview'); }
  getDashboardSites() { return this.request<ItemResponse<SiteRisk>>('/api/dashboard/sites'); }
  getDashboardActivities() { return this.request<ItemResponse<ActivityRisk>>('/api/dashboard/activities'); }
  getDashboardRules() { return this.request<ItemResponse<RuleDistribution>>('/api/dashboard/rules'); }
  getDashboardPrecursors() { return this.request<ItemResponse<Precursor>>('/api/dashboard/precursors'); }
}

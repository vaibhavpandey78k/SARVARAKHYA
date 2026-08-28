import type { Analysis } from '../types/api';
import { ConfidenceBadge, ReviewStatus, RuleBadge, SIFBadge, Section } from './ui';
export default function AnalysisResult({analysis}:{analysis:Analysis}){
  const score = typeof analysis.sif_probability === 'number' ? analysis.sif_probability : 0;
  const label = analysis.sif_probability === analysis.sif_score ? 'Baseline heuristic score (not calibrated probability)' : 'SIF probability returned by AI service';
  return <div className="analysis-grid">
    <Section title="Prediction"><div className="prediction"><SIFBadge value={analysis.sif_prediction}/><div className="prob"><strong>{(score*100).toFixed(0)}%</strong><span>{label}</span></div><ConfidenceBadge value={analysis.confidence}/></div>{analysis.model_version&&<div className="muted" style={{marginTop:8}}>Model: {analysis.model_version} · Analysis: {analysis.analysis_type||'baseline'}</div>}</Section>
    <Section title="Operational context"><div className="facts"><div><span>Activity</span><strong>{analysis.activity||'Not available'}</strong></div><div><span>Location</span><strong>{analysis.location||'Not available'}</strong></div><div><span>Barrier failure</span><strong>{analysis.barrier_failure||'Not available'}</strong></div><div><span>Review</span><ReviewStatus value={analysis.review_status}/></div></div></Section>
    <Section title="Life-Saving Rule(s)"><div className="tags">{analysis.life_saving_rules.length?analysis.life_saving_rules.map(x=><RuleBadge key={x}>{x}</RuleBadge>):<span className="muted">None returned</span>}</div></Section>
    <Section title="Supporting evidence"><ul className="evidence">{analysis.evidence?.length?analysis.evidence.map((e,i)=><li key={i}>{e}</li>):<li className="muted">No evidence returned.</li>}</ul></Section>
  </div>
}

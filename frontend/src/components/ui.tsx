import type { ReactNode } from 'react';
import { AlertTriangle, CheckCircle2, Loader2, SearchX } from 'lucide-react';

export const LoadingState=({label='Loading…'}:{label?:string})=><div className="state"><Loader2 className="spin" size={22}/><span>{label}</span></div>;
export const EmptyState=({title='No data available',text='There is nothing to display yet.'}:{title?:string;text?:string})=><div className="state empty"><SearchX size={28}/><strong>{title}</strong><span>{text}</span></div>;
export const ErrorState=({title='Something went wrong',text='Please try again or check the backend connection.',onRetry}:{title?:string;text?:string;onRetry?:()=>void})=><div className="state error"><AlertTriangle size={28}/><strong>{title}</strong><span>{text}</span>{onRetry&&<button className="button secondary" onClick={onRetry}>Retry</button>}</div>;
export const SIFBadge=({value}:{value:boolean|null|undefined})=><span className={`badge ${value===true?'danger':value===null?'confidence':'safe'}`}>{value===undefined?'Not analyzed':value===null?'Uncertain':value?'SIF Potential':'Non-SIF Potential'}</span>;
export const ConfidenceBadge=({value}:{value?:string})=><span className={`badge confidence ${String(value||'').toLowerCase()}`}>{value||'Not available'} confidence</span>;
export const RuleBadge=({children}:{children:ReactNode})=><span className="rule">{children}</span>;
export const ReviewStatus=({value}:{value?:string})=><span className={`status ${String(value||'').toLowerCase().replace(/ /g,'-')}`}>{value||'Not available'}</span>;
export const Section=({title,children,action}:{title:string;children:ReactNode;action?:ReactNode})=><section className="panel"><div className="panel-head"><h2>{title}</h2>{action}</div>{children}</section>;

import type { ReactNode } from 'react';
export default function RiskCard({label,value,sub,icon}:{label:string;value:ReactNode;sub?:string;icon?:ReactNode}){return <div className="kpi"><div className="kpi-top"><span>{label}</span><span className="kpi-icon">{icon}</span></div><strong>{value}</strong>{sub&&<small>{sub}</small>}</div>}

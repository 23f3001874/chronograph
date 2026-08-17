import React from 'react';
import { CheckCircle2, AlertTriangle, HelpCircle, XCircle, Clock, ShieldCheck } from 'lucide-react';

export default function EpistemicBadge({ status }) {
  if (!status) return null;

  const st = status.toUpperCase();

  let className = 'badge-unknown';
  let icon = <HelpCircle size={14} />;
  let label = st;

  switch (st) {
    case 'SUPPORTED':
    case 'ACTIVE':
      className = 'badge-supported';
      icon = <ShieldCheck size={14} />;
      break;
    case 'SUPERSEDED':
      className = 'badge-superseded';
      icon = <Clock size={14} />;
      break;
    case 'CONFLICTED':
      className = 'badge-conflicted';
      icon = <AlertTriangle size={14} />;
      break;
    case 'CANCELLED':
      className = 'badge-cancelled';
      icon = <XCircle size={14} />;
      break;
    case 'UNKNOWN':
      className = 'badge-unknown';
      icon = <HelpCircle size={14} />;
      break;
    default:
      break;
  }

  return (
    <span className={`badge ${className}`}>
      {icon}
      {label}
    </span>
  );
}

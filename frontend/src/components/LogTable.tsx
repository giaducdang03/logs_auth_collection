import { LogRecord } from '../api/client';

interface LogTableProps {
  logs: LogRecord[];
}

export const LogTable = ({ logs }: LogTableProps) => {
  const formatDate = (dateString: string) => {
    // API returns UTC timestamps (e.g. 2026-04-06T22:54:12Z).
    // Parse as UTC then format in the browser's local timezone.
    const normalized = dateString.includes(' ') ? dateString.replace(' ', 'T') : dateString;
    const utcSource = /Z$|[+-]\d{2}:\d{2}$/.test(normalized)
      ? normalized
      : `${normalized}Z`;

    const date = new Date(utcSource);
    if (Number.isNaN(date.getTime())) {
      return dateString;
    }

    const browserTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const parts = new Intl.DateTimeFormat('en-GB', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
      timeZone: browserTimeZone,
    }).formatToParts(date);

    const get = (type: Intl.DateTimeFormatPartTypes) => parts.find((p) => p.type === type)?.value ?? '';
    const formatted = `${get('day')}/${get('month')}/${get('year')} ${get('hour')}:${get('minute')}:${get('second')}`;

    return `${formatted} (${browserTimeZone})`;
  };

  const getStatusBadgeClass = (status: string) => {
    return status === 'success'
      ? 'bg-emerald-100 text-emerald-800 ring-emerald-600/20'
      : 'bg-rose-100 text-rose-800 ring-rose-600/20';
  };

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Timestamp</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Username</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">IP Address</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Status</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">Auth Method</th>
            <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">SSH Key</th>
          </tr>
        </thead>
          <tbody className="divide-y divide-slate-100 bg-white">
          {logs.map((log) => (
            <tr key={log.id} className="transition hover:bg-slate-50">
              <td className="whitespace-nowrap px-4 py-3 text-sm text-slate-700">{formatDate(log.login_time)}</td>
              <td className="px-4 py-3 text-sm font-medium text-black">{log.username || '-'}</td>
              <td className="px-4 py-3 font-mono text-sm text-cyan-700">{log.ip_address || '-'}</td>
              <td className="px-4 py-3 text-sm">
                <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ring-inset ${getStatusBadgeClass(log.status)}`}>
                  {log.status}
                </span>
              </td>
              <td className="px-4 py-3 text-sm capitalize text-slate-600">{log.auth_method || 'unknown'}</td>
              <td className="max-w-[280px] truncate px-4 py-3 font-mono text-xs text-slate-600" title={log.ssh_key || '-'}>{log.ssh_key || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </div>
  );
};

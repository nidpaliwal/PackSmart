export default function CompliancePanel({ notes }) {
  if (!notes || notes.length === 0) return null;

  const warnings = notes.filter((n) => n.severity === 'critical' || n.severity === 'warning');
  const info = notes.filter((n) => n.severity !== 'critical' && n.severity !== 'warning');

  return (
    <div className="bg-white rounded-xl shadow-sm border p-5">
      <h3 className="font-semibold text-gray-900 mb-3">Compliance & Regulatory Notes</h3>

      {warnings.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-amber-700 mb-2">Warnings</h4>
          <div className="space-y-2">
            {warnings.map((w, i) => (
              <div key={i} className="text-sm bg-amber-50 border border-amber-200 rounded-lg p-3">
                <p className="text-amber-800">{w.message}</p>
                <p className="text-xs text-amber-600 mt-1">{w.citation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {info.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-blue-700 mb-2">Information</h4>
          <div className="space-y-2">
            {info.map((n, i) => (
              <div key={i} className="text-sm bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p className="text-blue-800">{n.message}</p>
                <p className="text-xs text-blue-600 mt-1">{n.citation}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

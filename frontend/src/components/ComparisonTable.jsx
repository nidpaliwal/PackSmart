import { useTranslation } from '../App';

export default function ComparisonTable({ recommendations }) {
  const t = useTranslation();

  if (!recommendations || recommendations.length === 0) return null;

  const metrics = [
    { key: 'score', label: t.score, format: (v) => `${Math.round(v * 100)}%` },
    { key: 'barrier_score', label: t.barrier, format: (v) => `${Math.round(v * 100)}%` },
    { key: 'shelf_life_score', label: 'SL Fit', format: (v) => `${Math.round(v * 100)}%` },
    { key: 'cost_score', label: 'Cost Eff.', format: (v) => `${Math.round(v * 100)}%` },
    { key: 'sustainability_score', label: t.sustainability_label, format: (v) => `${Math.round(v * 100)}%` },
    { key: 'practicality_score', label: 'Practical', format: (v) => `${Math.round(v * 100)}%` },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border p-5">
      <h3 className="font-semibold text-gray-900 mb-4">Side-by-Side Comparison</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b">
              <th className="text-left py-2 pr-4 font-medium text-gray-600">Metric</th>
              {recommendations.map((rec) => (
                <th key={rec.material_id} className="text-center py-2 px-3 font-medium text-gray-900">
                  <div className="truncate max-w-[120px]">{rec.material_name}</div>
                  <div className="text-xs text-gray-400 font-normal">Rank #{rec.rank}</div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {metrics.map((m) => (
              <tr key={m.key} className="border-b last:border-0">
                <td className="py-2 pr-4 text-gray-600">{m.label}</td>
                {recommendations.map((rec) => {
                  const val = rec[m.key] || 0;
                  const maxVal = Math.max(...recommendations.map((r) => r[m.key] || 0));
                  const isBest = val === maxVal && val > 0;
                  return (
                    <td key={rec.material_id} className="text-center py-2 px-3">
                      <span className={`font-medium ${isBest ? 'text-green-600' : 'text-gray-700'}`}>
                        {m.format(val)}
                      </span>
                    </td>
                  );
                })}
              </tr>
            ))}
            <tr className="border-b">
              <td className="py-2 pr-4 text-gray-600">{t.shelf_life}</td>
              {recommendations.map((rec) => (
                <td key={rec.material_id} className="text-center py-2 px-3 font-medium">
                  {rec.shelf_life.min_days}-{rec.shelf_life.max_days} {t.days}
                </td>
              ))}
            </tr>
            <tr className="border-b">
              <td className="py-2 pr-4 text-gray-600">{t.cost_per_unit}</td>
              {recommendations.map((rec) => (
                <td key={rec.material_id} className="text-center py-2 px-3 font-medium">
                  Rs. {rec.cost_per_unit?.toFixed(1)}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-2 pr-4 text-gray-600">Model</td>
              {recommendations.map((rec) => (
                <td key={rec.material_id} className="text-center py-2 px-3 text-xs text-gray-500">
                  {rec.shelf_life.model_used}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

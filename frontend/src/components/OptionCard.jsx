import { useTranslation } from '../App';

export default function OptionCard({ rec }) {
  const t = useTranslation();

  const rankColors = {
    1: 'bg-yellow-400 text-yellow-900',
    2: 'bg-gray-300 text-gray-700',
    3: 'bg-orange-300 text-orange-900',
  };

  const scorePercent = Math.round(rec.score * 100);

  return (
    <div className="bg-white rounded-xl shadow-sm border p-5 relative">
      <div className={`absolute -top-3 -left-3 w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${rankColors[rec.rank] || 'bg-gray-200'}`}>
        #{rec.rank}
      </div>

      <h3 className="font-semibold text-gray-900 mt-2 mb-1 text-sm leading-tight">
        {rec.material_name}
      </h3>

      <div className="mb-3">
        <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
          <span>{t.score}</span>
          <span className="font-semibold text-gray-900">{scorePercent}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all"
            style={{ width: `${scorePercent}%` }}
          />
        </div>
      </div>

      <div className="space-y-2 text-xs">
        <div className="flex justify-between">
          <span className="text-gray-500">{t.shelf_life}</span>
          <span className="font-medium">{rec.shelf_life.min_days}-{rec.shelf_life.max_days} {t.days}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">{t.cost_per_unit}</span>
          <span className="font-medium">Rs. {rec.cost_per_unit?.toFixed(1)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">{t.barrier}</span>
          <span className="font-medium">{Math.round(rec.barrier_score * 100)}%</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">{t.sustainability_label}</span>
          <span className="font-medium">{Math.round(rec.sustainability_score * 100)}%</span>
        </div>
      </div>

      {rec.is_multi_layer && (
        <span className="inline-block mt-2 px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded">
          {t.multi_layer}
        </span>
      )}

      <p className="mt-3 text-xs text-gray-600 leading-relaxed">
        {rec.explanation}
      </p>

      {rec.warnings.length > 0 && (
        <div className="mt-3 space-y-1">
          {rec.warnings.map((w, i) => (
            <div key={i} className="text-xs text-amber-700 bg-amber-50 rounded px-2 py-1">
              {w}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

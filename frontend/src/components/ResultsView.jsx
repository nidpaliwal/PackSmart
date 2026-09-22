import OptionCard from './OptionCard';
import CompliancePanel from './CompliancePanel';
import { useTranslation } from '../App';

export default function ResultsView({ data, onReset }) {
  const t = useTranslation();

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900">
            {t.recommendations_for} {data.commodity_name}
          </h2>
          <p className="text-sm text-gray-500 mt-1">Session: {data.session_id}</p>
        </div>
        <button
          onClick={onReset}
          className="px-4 py-2 text-sm font-medium text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50"
        >
          {t.new_recommendation}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {data.recommendations.map((rec) => (
          <OptionCard key={rec.material_id} rec={rec} />
        ))}
      </div>

      <CompliancePanel notes={data.compliance_notes} />

      <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-sm text-yellow-800">
        {data.disclaimer}
      </div>
    </div>
  );
}

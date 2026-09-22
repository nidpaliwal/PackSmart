import { useState } from 'react';
import OptionCard from './OptionCard';
import CompliancePanel from './CompliancePanel';
import ComparisonTable from './ComparisonTable';
import WhatIfPanel from './WhatIfPanel';
import { useTranslation } from '../App';

export default function ResultsView({ data, onReset, onWhatIf }) {
  const t = useTranslation();
  const noResults = !data.recommendations || data.recommendations.length === 0;

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

      {noResults ? (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-8 text-center mb-8">
          <div className="text-4xl mb-3">📦</div>
          <h3 className="text-lg font-semibold text-amber-800 mb-2">{t.no_results_title}</h3>
          <p className="text-amber-700 mb-4">{t.no_results_message}</p>
          <button
            onClick={onReset}
            className="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 text-sm font-medium"
          >
            {t.try_different_inputs}
          </button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            {data.recommendations.map((rec) => (
              <OptionCard key={rec.material_id} rec={rec} />
            ))}
          </div>

          <div className="mb-8">
            <ComparisonTable recommendations={data.recommendations} />
          </div>

          <div className="mb-8">
            <WhatIfPanel sessionId={data.session_id} onWhatIf={onWhatIf} />
          </div>
        </>
      )}

      <CompliancePanel notes={data.compliance_notes} />

      <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-sm text-yellow-800">
        {data.disclaimer}
      </div>
    </div>
  );
}

import { useState } from 'react';
import { useTranslation } from '../App';
import { DEFAULT_WEIGHTS } from './ComparisonTable';

export default function WhatIfPanel({ sessionId, onWhatIf }) {
  const t = useTranslation();
  const [open, setOpen] = useState(false);
  const [weights, setWeights] = useState({ ...DEFAULT_WEIGHTS });
  const [targetDays, setTargetDays] = useState('');
  const [temp, setTemp] = useState('');
  const [budget, setBudget] = useState('');

  const updateWeight = (key, val) => {
    setWeights((prev) => ({ ...prev, [key]: Math.max(0, Math.min(1, Number(val) || 0)) }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = { session_id: sessionId, weights };
    if (targetDays) payload.shelf_life_target_days = parseInt(targetDays, 10);
    if (temp) payload.storage_temp_c = parseFloat(temp);
    if (budget) payload.budget_per_unit = parseFloat(budget);
    onWhatIf(payload);
  };

  return (
    <div className="bg-white rounded-xl border shadow-sm">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-4 text-left"
      >
        <span className="text-sm font-semibold text-gray-800">{t.what_if_title}</span>
        <span className="text-gray-400">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <form onSubmit={handleSubmit} className="px-4 pb-4 border-t">
          <p className="text-xs text-gray-500 mb-3">{t.what_if_description}</p>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-4">
            {Object.entries(DEFAULT_WEIGHTS).map(([key]) => (
              <div key={key}>
                <label className="block text-xs font-medium text-gray-600 mb-1 capitalize">{key}</label>
                <input
                  type="number"
                  step="0.05"
                  min="0"
                  max="1"
                  value={weights[key]}
                  onChange={(e) => updateWeight(key, e.target.value)}
                  className="w-full border rounded px-2 py-1.5 text-sm"
                />
              </div>
            ))}
          </div>

          <div className="grid grid-cols-3 gap-3 mb-4">
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">{t.shelf_life_target} (override)</label>
              <input
                type="number"
                min="1"
                value={targetDays}
                onChange={(e) => setTargetDays(e.target.value)}
                placeholder={t.optional}
                className="w-full border rounded px-2 py-1.5 text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">{t.storage_temp} (override)</label>
              <input
                type="number"
                value={temp}
                onChange={(e) => setTemp(e.target.value)}
                placeholder={t.optional}
                className="w-full border rounded px-2 py-1.5 text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-600 mb-1">{t.budget} (override)</label>
              <input
                type="number"
                step="0.5"
                min="0"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                placeholder={t.optional}
                className="w-full border rounded px-2 py-1.5 text-sm"
              />
            </div>
          </div>

          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700"
          >
            {t.re_rank}
          </button>
        </form>
      )}
    </div>
  );
}

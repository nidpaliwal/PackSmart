import { useState, useEffect } from 'react';
import { fetchCommodities, fetchCategories } from '../api';
import { useTranslation } from '../App';

export default function StepWizard({ onSubmit }) {
  const t = useTranslation();
  const [step, setStep] = useState(0);
  const [categories, setCategories] = useState([]);
  const [commodities, setCommodities] = useState([]);
  const [loading, setLoading] = useState(false);

  const STEPS = [t.step1, t.step2, t.step3];

  const [form, setForm] = useState({
    commodity_id: null,
    commodity_name: '',
    shelf_life_target_days: 30,
    pack_size_g: 500,
    storage_temp_c: 25,
    storage_humidity_pct: 60,
    transport_mode: 'road',
    transport_duration_days: 1,
    budget_per_unit: null,
    sustainability_priority: 'medium',
  });

  useEffect(() => {
    fetchCategories().then(setCategories).catch(() => {});
    setLoading(true);
    fetchCommodities().then(setCommodities).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const updateField = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const loadCommodities = async (category) => {
    setLoading(true);
    try {
      const data = await fetchCommodities(category || undefined);
      setCommodities(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const selectCommodity = (c) => {
    updateField('commodity_id', c.id);
    updateField('commodity_name', c.name);
    if (c.base_shelf_life_days) {
      updateField('shelf_life_target_days', c.base_shelf_life_days);
    }
  };

  const canNext = () => {
    if (step === 0) return form.commodity_id !== null;
    if (step === 1) return form.shelf_life_target_days > 0 && form.pack_size_g > 0;
    return true;
  };

  const handleSubmit = () => {
    onSubmit({
      commodity_id: form.commodity_id,
      shelf_life_target_days: form.shelf_life_target_days,
      pack_size_g: form.pack_size_g,
      storage_temp_c: form.storage_temp_c,
      storage_humidity_pct: form.storage_humidity_pct,
      transport_mode: form.transport_mode,
      transport_duration_days: form.transport_duration_days,
      budget_per_unit: form.budget_per_unit,
      sustainability_priority: form.sustainability_priority,
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6">
      <div className="flex items-center justify-between mb-6">
        {STEPS.map((s, i) => (
          <div key={i} className="flex items-center">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                i <= step ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'
              }`}
            >
              {i + 1}
            </div>
            <span className={`ml-2 text-sm hidden md:inline ${i <= step ? 'text-gray-900' : 'text-gray-400'}`}>
              {s}
            </span>
            {i < STEPS.length - 1 && (
              <div className={`w-8 md:w-16 h-0.5 mx-2 ${i < step ? 'bg-blue-600' : 'bg-gray-200'}`} />
            )}
          </div>
        ))}
      </div>

      {step === 0 && (
        <div>
          <h2 className="text-lg font-semibold mb-4">{t.select_food}</h2>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">{t.category}</label>
            <select
              className="w-full border rounded-lg px-3 py-2"
              onChange={(e) => {
                updateField('commodity_id', null);
                updateField('commodity_name', '');
                loadCommodities(e.target.value);
              }}
            >
              <option value="">{t.all_categories}</option>
              {categories.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {commodities.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-64 overflow-y-auto">
              {commodities.map((c) => (
                <button
                  key={c.id}
                  onClick={() => selectCommodity(c)}
                  className={`text-left p-3 rounded-lg border transition ${
                    form.commodity_id === c.id
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-400'
                  }`}
                >
                  <div className="font-medium text-sm">{c.name}</div>
                  <div className="text-xs text-gray-500">{c.category}</div>
                </button>
              ))}
            </div>
          )}

          {commodities.length === 0 && !loading && (
            <p className="text-gray-500 text-sm">{t.no_data}</p>
          )}
          {loading && <p className="text-gray-400 text-sm">{t.loading}</p>}
        </div>
      )}

      {step === 1 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold mb-4">{t.step2}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.shelf_life_target}</label>
              <input
                type="number"
                min="1"
                value={form.shelf_life_target_days}
                onChange={(e) => updateField('shelf_life_target_days', parseInt(e.target.value) || 1)}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.pack_size}</label>
              <input
                type="number"
                min="1"
                value={form.pack_size_g}
                onChange={(e) => updateField('pack_size_g', parseFloat(e.target.value) || 1)}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.storage_temp}</label>
              <input
                type="number"
                value={form.storage_temp_c}
                onChange={(e) => updateField('storage_temp_c', parseFloat(e.target.value) || 0)}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.storage_humidity}</label>
              <input
                type="number"
                min="0"
                max="100"
                value={form.storage_humidity_pct}
                onChange={(e) => updateField('storage_humidity_pct', parseFloat(e.target.value) || 0)}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.transport_mode}</label>
              <select
                value={form.transport_mode}
                onChange={(e) => updateField('transport_mode', e.target.value)}
                className="w-full border rounded-lg px-3 py-2"
              >
                <option value="road">{t.road}</option>
                <option value="rail">{t.rail}</option>
                <option value="air">{t.air}</option>
                <option value="sea">{t.sea}</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.transport_duration}</label>
              <input
                type="number"
                min="0"
                value={form.transport_duration_days}
                onChange={(e) => updateField('transport_duration_days', parseFloat(e.target.value) || 0)}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold mb-4">{t.step3}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.budget}</label>
              <input
                type="number"
                min="0"
                value={form.budget_per_unit || ''}
                onChange={(e) => updateField('budget_per_unit', parseFloat(e.target.value) || null)}
                placeholder={t.budget_optional}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t.sustainability}</label>
              <select
                value={form.sustainability_priority}
                onChange={(e) => updateField('sustainability_priority', e.target.value)}
                className="w-full border rounded-lg px-3 py-2"
              >
                <option value="low">{t.low}</option>
                <option value="medium">{t.medium}</option>
                <option value="high">{t.high}</option>
              </select>
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4 mt-4">
            <h3 className="text-sm font-medium text-gray-700 mb-2">{t.summary}</h3>
            <p className="text-sm text-gray-600">
              <strong>{form.commodity_name}</strong> | {form.shelf_life_target_days}{t.days} |{' '}
              {form.pack_size_g}g | {form.storage_temp_c}°C, {form.storage_humidity_pct}%
            </p>
          </div>
        </div>
      )}

      <div className="flex justify-between mt-8">
        <button
          onClick={() => setStep(Math.max(0, step - 1))}
          disabled={step === 0}
          className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 disabled:opacity-30"
        >
          {t.back}
        </button>
        {step < 2 ? (
          <button
            onClick={() => setStep(step + 1)}
            disabled={!canNext()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {t.next}
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            className="px-6 py-2 bg-green-600 text-white rounded-lg text-sm font-medium hover:bg-green-700"
          >
            {t.get_recommendations}
          </button>
        )}
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { useTranslation } from '../App';

const TABS = ['Commodities', 'Materials', 'Rules'];

export default function AdminPanel() {
  const t = useTranslation();
  const [tab, setTab] = useState(0);
  const [commodities, setCommodities] = useState([]);
  const [materials, setMaterials] = useState([]);
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [c, m, r] = await Promise.all([
        fetch('/api/commodities/').then((res) => res.json()),
        fetch('/api/materials/').then((res) => res.json()),
        fetch('/api/rules/').then((res) => res.json()),
      ]);
      setCommodities(c);
      setMaterials(m);
      setRules(r);
    } catch (e) {
      console.error('Failed to load admin data', e);
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (type, id) => {
    if (!confirm('Delete this item?')) return;
    try {
      await fetch(`/api/${type}/${id}`, { method: 'DELETE' });
      loadData();
    } catch (e) {
      console.error('Delete failed', e);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6">
      <h2 className="text-lg font-semibold mb-4">Knowledge Base Editor</h2>

      <div className="flex gap-2 mb-4 border-b">
        {TABS.map((label, i) => (
          <button
            key={label}
            onClick={() => setTab(i)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
              tab === i
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {label} ({i === 0 ? commodities.length : i === 1 ? materials.length : rules.length})
          </button>
        ))}
      </div>

      {tab === 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-3 py-2 font-medium">ID</th>
                <th className="px-3 py-2 font-medium">Name</th>
                <th className="px-3 py-2 font-medium">Category</th>
                <th className="px-3 py-2 font-medium">Moisture %</th>
                <th className="px-3 py-2 font-medium">Water Activity</th>
                <th className="px-3 py-2 font-medium">O2 Sensitive</th>
                <th className="px-3 py-2 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {commodities.map((c) => (
                <tr key={c.id} className="border-t hover:bg-gray-50">
                  <td className="px-3 py-2">{c.id}</td>
                  <td className="px-3 py-2 font-medium">{c.name}</td>
                  <td className="px-3 py-2">{c.category}</td>
                  <td className="px-3 py-2">{c.moisture_pct}</td>
                  <td className="px-3 py-2">{c.water_activity}</td>
                  <td className="px-3 py-2">{c.oxygen_sensitive ? 'Yes' : 'No'}</td>
                  <td className="px-3 py-2">
                    <button
                      onClick={() => deleteItem('commodities', c.id)}
                      className="text-red-600 hover:text-red-800 text-xs"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 1 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-3 py-2 font-medium">ID</th>
                <th className="px-3 py-2 font-medium">Name</th>
                <th className="px-3 py-2 font-medium">Type</th>
                <th className="px-3 py-2 font-medium">WVTR</th>
                <th className="px-3 py-2 font-medium">OTR</th>
                <th className="px-3 py-2 font-medium">Cost/m²</th>
                <th className="px-3 py-2 font-medium">Recyclability</th>
                <th className="px-3 py-2 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {materials.map((m) => (
                <tr key={m.id} className="border-t hover:bg-gray-50">
                  <td className="px-3 py-2">{m.id}</td>
                  <td className="px-3 py-2 font-medium">{m.name}</td>
                  <td className="px-3 py-2">{m.material_type}</td>
                  <td className="px-3 py-2">{m.wvtr}</td>
                  <td className="px-3 py-2">{m.otr}</td>
                  <td className="px-3 py-2">Rs. {m.cost_per_m2}</td>
                  <td className="px-3 py-2">{m.recyclability}</td>
                  <td className="px-3 py-2">
                    <button
                      onClick={() => deleteItem('materials', m.id)}
                      className="text-red-600 hover:text-red-800 text-xs"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === 2 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left">
                <th className="px-3 py-2 font-medium">ID</th>
                <th className="px-3 py-2 font-medium">Scope</th>
                <th className="px-3 py-2 font-medium">Condition</th>
                <th className="px-3 py-2 font-medium">Severity</th>
                <th className="px-3 py-2 font-medium">Message</th>
                <th className="px-3 py-2 font-medium">Citation</th>
                <th className="px-3 py-2 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rules.map((r) => (
                <tr key={r.id} className="border-t hover:bg-gray-50">
                  <td className="px-3 py-2">{r.id}</td>
                  <td className="px-3 py-2">{r.scope_type}</td>
                  <td className="px-3 py-2">{r.condition_type}</td>
                  <td className="px-3 py-2">
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      r.severity === 'critical' ? 'bg-red-100 text-red-700' :
                      r.severity === 'warning' ? 'bg-amber-100 text-amber-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {r.severity}
                    </span>
                  </td>
                  <td className="px-3 py-2 max-w-xs truncate">{r.message}</td>
                  <td className="px-3 py-2 text-xs text-gray-500">{r.regulation_citation}</td>
                  <td className="px-3 py-2">
                    <button
                      onClick={() => deleteItem('rules', r.id)}
                      className="text-red-600 hover:text-red-800 text-xs"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

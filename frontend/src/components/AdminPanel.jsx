import { useState, useEffect } from 'react';
import { useTranslation } from '../App';

const TABS = ['Commodities', 'Materials', 'Rules'];

function AdminTokenGate({ onToken }) {
  const t = useTranslation();
  const [token, setToken] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('/api/commodities/', {
        headers: { 'X-Admin-Token': token },
      });
      if (res.ok) {
        onToken(token);
      } else if (res.status === 401 || res.status === 403) {
        setError('Invalid admin token');
      } else {
        setError('Unexpected error');
      }
    } catch {
      setError('Connection failed');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6 max-w-md mx-auto text-center">
      <div className="text-3xl mb-3">🔒</div>
      <h2 className="text-lg font-semibold text-gray-900 mb-2">{t.admin_login_title}</h2>
      <p className="text-sm text-gray-500 mb-4">{t.admin_login_description}</p>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="password"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder={t.admin_token_placeholder}
          required
          className="flex-1 border rounded-lg px-3 py-2 text-sm"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700"
        >
          {t.admin_login_button}
        </button>
      </form>
      {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
    </div>
  );
}

function CommodityForm({ token, onSaved }) {
  const [form, setForm] = useState({
    name: '', category: '', moisture_pct: '', water_activity: '', oxygen_sensitive: false,
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const payload = {
      name: form.name.trim(),
      category: form.category.trim(),
      moisture_pct: parseFloat(form.moisture_pct) || 0,
      water_activity: parseFloat(form.water_activity) || 0,
      oxygen_sensitive: form.oxygen_sensitive,
    };
    if (!payload.name || !payload.category) {
      setError('Name and category are required');
      return;
    }
    try {
      const res = await fetch('/api/commodities/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Admin-Token': token },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        setError(err.detail || 'Failed to save');
        return;
      }
      onSaved();
      setForm({ name: '', category: '', moisture_pct: '', water_activity: '', oxygen_sensitive: false });
    } catch {
      setError('Network error');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 text-sm">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <input name="name" value={form.name} onChange={handleChange} placeholder="Name *" required className="border rounded px-2 py-1.5" />
        <input name="category" value={form.category} onChange={handleChange} placeholder="Category *" required className="border rounded px-2 py-1.5" />
        <input name="moisture_pct" type="number" min="0" max="100" step="0.1" value={form.moisture_pct} onChange={handleChange} placeholder="Moisture %" className="border rounded px-2 py-1.5" />
        <input name="water_activity" type="number" min="0" max="1" step="0.01" value={form.water_activity} onChange={handleChange} placeholder="Water activity" className="border rounded px-2 py-1.5" />
        <label className="flex items-center gap-1 text-xs">
          <input type="checkbox" name="oxygen_sensitive" checked={form.oxygen_sensitive} onChange={handleChange} />
          O₂ sensitive
        </label>
      </div>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <button type="submit" className="mt-2 px-3 py-1.5 bg-blue-600 text-white rounded text-xs font-medium hover:bg-blue-700">Add Commodity</button>
    </form>
  );
}

function MaterialForm({ token, onSaved }) {
  const [form, setForm] = useState({
    name: '', material_type: '', wvtr: '', otr: '', cost_per_m2: '', recyclability: 'medium',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const payload = {
      name: form.name.trim(),
      material_type: form.material_type.trim(),
      wvtr: parseFloat(form.wvtr) || 0,
      otr: parseFloat(form.otr) || 0,
      cost_per_m2: parseFloat(form.cost_per_m2) || 0,
      recyclability: form.recyclability,
    };
    if (!payload.name || !payload.material_type) {
      setError('Name and type are required');
      return;
    }
    if (payload.cost_per_m2 < 0) {
      setError('Cost cannot be negative');
      return;
    }
    try {
      const res = await fetch('/api/materials/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Admin-Token': token },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        setError(err.detail || 'Failed to save');
        return;
      }
      onSaved();
      setForm({ name: '', material_type: '', wvtr: '', otr: '', cost_per_m2: '', recyclability: 'medium' });
    } catch {
      setError('Network error');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 text-sm">
      <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
        <input name="name" value={form.name} onChange={handleChange} placeholder="Name *" required className="border rounded px-2 py-1.5" />
        <input name="material_type" value={form.material_type} onChange={handleChange} placeholder="Type *" required className="border rounded px-2 py-1.5" />
        <input name="wvtr" type="number" min="0" step="0.01" value={form.wvtr} onChange={handleChange} placeholder="WVTR" className="border rounded px-2 py-1.5" />
        <input name="otr" type="number" min="0" step="0.01" value={form.otr} onChange={handleChange} placeholder="OTR" className="border rounded px-2 py-1.5" />
        <input name="cost_per_m2" type="number" min="0" step="0.5" value={form.cost_per_m2} onChange={handleChange} placeholder="Cost/m² *" required className="border rounded px-2 py-1.5" />
        <select name="recyclability" value={form.recyclability} onChange={handleChange} className="border rounded px-2 py-1.5">
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <button type="submit" className="mt-2 px-3 py-1.5 bg-blue-600 text-white rounded text-xs font-medium hover:bg-blue-700">Add Material</button>
    </form>
  );
}

function RuleForm({ token, onSaved }) {
  const [form, setForm] = useState({
    scope_type: 'commodity', condition_type: '', message: '', regulation_citation: '', severity: 'warning',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const payload = {
      scope_type: form.scope_type,
      condition_type: form.condition_type.trim(),
      message: form.message.trim(),
      regulation_citation: form.regulation_citation.trim(),
      severity: form.severity,
    };
    if (!payload.condition_type || !payload.message) {
      setError('Condition and message are required');
      return;
    }
    try {
      const res = await fetch('/api/rules/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Admin-Token': token },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        setError(err.detail || 'Failed to save');
        return;
      }
      onSaved();
      setForm({ scope_type: 'commodity', condition_type: '', message: '', regulation_citation: '', severity: 'warning' });
    } catch {
      setError('Network error');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4 mb-4 text-sm">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <select name="scope_type" value={form.scope_type} onChange={handleChange} className="border rounded px-2 py-1.5">
          <option value="commodity">Commodity</option>
          <option value="material">Material</option>
        </select>
        <input name="condition_type" value={form.condition_type} onChange={handleChange} placeholder="Condition *" required className="border rounded px-2 py-1.5" />
        <input name="message" value={form.message} onChange={handleChange} placeholder="Message *" required className="border rounded px-2 py-1.5" />
        <input name="regulation_citation" value={form.regulation_citation} onChange={handleChange} placeholder="Citation" className="border rounded px-2 py-1.5" />
        <select name="severity" value={form.severity} onChange={handleChange} className="border rounded px-2 py-1.5">
          <option value="critical">Critical</option>
          <option value="warning">Warning</option>
          <option value="info">Info</option>
        </select>
      </div>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <button type="submit" className="mt-2 px-3 py-1.5 bg-blue-600 text-white rounded text-xs font-medium hover:bg-blue-700">Add Rule</button>
    </form>
  );
}

export default function AdminPanel() {
  const t = useTranslation();
  const [token, setToken] = useState(null);
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
      await fetch(`/api/${type}/${id}`, {
        method: 'DELETE',
        headers: { 'X-Admin-Token': token },
      });
      loadData();
    } catch (e) {
      console.error('Delete failed', e);
    }
  };

  if (!token) {
    return <AdminTokenGate onToken={setToken} />;
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">Knowledge Base Editor</h2>
        <button onClick={() => setToken(null)} className="text-xs text-gray-500 hover:text-gray-700">🔒 Lock</button>
      </div>

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
        <>
          <CommodityForm token={token} onSaved={loadData} />
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
        </>
      )}

      {tab === 1 && (
        <>
          <MaterialForm token={token} onSaved={loadData} />
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
        </>
      )}

      {tab === 2 && (
        <>
          <RuleForm token={token} onSaved={loadData} />
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
        </>
      )}
    </div>
  );
}

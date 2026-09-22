const API_BASE = '/api';

export async function fetchCommodities(category) {
  const url = category
    ? `${API_BASE}/commodities/?category=${encodeURIComponent(category)}`
    : `${API_BASE}/commodities/`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch commodities');
  return res.json();
}

export async function fetchCommodity(id) {
  const res = await fetch(`${API_BASE}/commodities/${id}`);
  if (!res.ok) throw new Error('Failed to fetch commodity');
  return res.json();
}

export async function fetchMaterials() {
  const res = await fetch(`${API_BASE}/materials/`);
  if (!res.ok) throw new Error('Failed to fetch materials');
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${API_BASE}/commodities/categories/list`);
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function getRecommendation(data) {
  const res = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Recommendation failed');
  }
  return res.json();
}

import { useState, createContext, useContext } from 'react';
import StepWizard from './components/StepWizard';
import ResultsView from './components/ResultsView';
import AdminPanel from './components/AdminPanel';
import { getRecommendation, getWhatIf } from './api';
import translations from './translations';

export const LanguageContext = createContext();

export function useTranslation() {
  const { lang } = useContext(LanguageContext);
  return translations[lang] || translations.en;
}

export default function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lang, setLang] = useState('en');
  const [page, setPage] = useState('home');

  const t = translations[lang] || translations.en;

  const handleSubmit = async (inputs) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRecommendation(inputs);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleWhatIf = async (whatIfData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getWhatIf(whatIfData);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setPage('home');
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang }}>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-blue-600 text-white py-6 px-4 shadow-md">
          <div className="max-w-5xl mx-auto flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold cursor-pointer" onClick={() => setPage('home')}>
                {t.app_title}
              </h1>
              <p className="text-blue-100 text-sm mt-1">{t.app_subtitle}</p>
            </div>
            <div className="flex items-center gap-3">
              <nav className="flex gap-2 text-sm">
                <button
                  onClick={() => setPage('home')}
                  className={`px-3 py-1 rounded ${page === 'home' ? 'bg-blue-700' : 'hover:bg-blue-500'}`}
                >
                  Recommend
                </button>
                <button
                  onClick={() => setPage('admin')}
                  className={`px-3 py-1 rounded ${page === 'admin' ? 'bg-blue-700' : 'hover:bg-blue-500'}`}
                >
                  Admin
                </button>
              </nav>
              <select
                value={lang}
                onChange={(e) => setLang(e.target.value)}
                className="bg-blue-700 text-white border border-blue-500 rounded px-2 py-1 text-sm"
              >
                <option value="en">English</option>
                <option value="hi">हिन्दी</option>
              </select>
            </div>
          </div>
        </header>

        <main className="max-w-5xl mx-auto py-8 px-4">
          {page === 'admin' ? (
            <AdminPanel />
          ) : (
            <>
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 text-red-700">
                  {error}
                </div>
              )}

              {loading && (
                <div className="text-center py-20">
                  <div className="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
                  <p className="mt-4 text-gray-600">{t.analyzing}</p>
                </div>
              )}

              {!loading && !results && (
                <StepWizard onSubmit={handleSubmit} />
              )}

              {!loading && results && (
                <ResultsView data={results} onReset={handleReset} onWhatIf={handleWhatIf} />
              )}
            </>
          )}
        </main>

        <footer className="bg-gray-100 border-t py-4 px-4 text-center text-sm text-gray-500">
          <p>{t.disclaimer}</p>
          <p className="mt-1">
            PackSmart v1.0 | Ministry of Food Processing Industries | SIH26236
          </p>
        </footer>
      </div>
    </LanguageContext.Provider>
  );
}

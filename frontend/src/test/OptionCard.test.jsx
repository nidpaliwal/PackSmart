import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { LanguageContext } from '../App';
import OptionCard from '../components/OptionCard';

const mockRec = {
  rank: 1,
  material_id: 1,
  material_name: 'Metallised PET',
  score: 0.85,
  barrier_score: 0.9,
  shelf_life_score: 0.8,
  cost_score: 0.7,
  sustainability_score: 0.6,
  practicality_score: 0.9,
  shelf_life: { min_days: 60, max_days: 100, model_used: 'Q10 oxidation model' },
  cost_per_unit: 5.5,
  warnings: [],
  explanation: 'Best barrier for chips.',
  is_multi_layer: false,
};

function renderWithProvider(ui) {
  return render(
    <LanguageContext.Provider value={{ lang: 'en', setLang: () => {} }}>
      {ui}
    </LanguageContext.Provider>
  );
}

describe('OptionCard', () => {
  it('renders material name', () => {
    renderWithProvider(<OptionCard rec={mockRec} />);
    expect(screen.getByText('Metallised PET')).toBeInTheDocument();
  });

  it('shows rank number', () => {
    renderWithProvider(<OptionCard rec={mockRec} />);
    expect(screen.getByText('#1')).toBeInTheDocument();
  });

  it('shows shelf life range', () => {
    renderWithProvider(<OptionCard rec={mockRec} />);
    expect(screen.getByText(/60-100/)).toBeInTheDocument();
  });

  it('shows cost', () => {
    renderWithProvider(<OptionCard rec={mockRec} />);
    expect(screen.getByText(/5\.5/)).toBeInTheDocument();
  });

  it('shows explanation', () => {
    renderWithProvider(<OptionCard rec={mockRec} />);
    expect(screen.getByText('Best barrier for chips.')).toBeInTheDocument();
  });

  it('renders warnings when present', () => {
    const recWithWarnings = { ...mockRec, warnings: ['Over-packaged: too much barrier'] };
    renderWithProvider(<OptionCard rec={recWithWarnings} />);
    expect(screen.getByText(/Over-packaged/)).toBeInTheDocument();
  });

  it('shows multi-layer badge when applicable', () => {
    const multiLayerRec = { ...mockRec, is_multi_layer: true };
    renderWithProvider(<OptionCard rec={multiLayerRec} />);
    expect(screen.getByText(/Multi-layer/)).toBeInTheDocument();
  });
});

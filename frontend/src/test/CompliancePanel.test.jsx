import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import CompliancePanel from '../components/CompliancePanel';

describe('CompliancePanel', () => {
  it('renders nothing when notes are empty', () => {
    const { container } = render(<CompliancePanel notes={[]} />);
    expect(container.innerHTML).toBe('');
  });

  it('renders warnings', () => {
    const notes = [
      { message: 'Material not suitable for acidic food', citation: 'FSSAI 2018, Reg 5', severity: 'warning' },
    ];
    render(<CompliancePanel notes={notes} />);
    expect(screen.getByText(/Material not suitable/)).toBeInTheDocument();
    expect(screen.getByText(/FSSAI 2018/)).toBeInTheDocument();
  });

  it('renders info notes', () => {
    const notes = [
      { message: 'Aluminium foil not recyclable', citation: 'PWM Rules 2016', severity: 'info' },
    ];
    render(<CompliancePanel notes={notes} />);
    expect(screen.getByText(/Aluminium foil/)).toBeInTheDocument();
  });

  it('renders critical warnings', () => {
    const notes = [
      { message: 'Material not food-contact safe', citation: 'FSSAI 2018, Reg 4', severity: 'critical' },
    ];
    render(<CompliancePanel notes={notes} />);
    expect(screen.getByText(/not food-contact safe/)).toBeInTheDocument();
  });
});

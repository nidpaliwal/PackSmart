import { describe, it, expect } from 'vitest';
import translations from '../translations';

describe('translations', () => {
  it('has English translations', () => {
    expect(translations.en).toBeDefined();
    expect(translations.en.app_title).toBe('PackSmart');
    expect(translations.en.step1).toBe('Food Selection');
    expect(translations.en.get_recommendations).toBe('Get Recommendations');
  });

  it('has Hindi translations', () => {
    expect(translations.hi).toBeDefined();
    expect(translations.hi.app_title).toBe('PackSmart');
    expect(translations.hi.step1).toBe('खाद्य चयन');
    expect(translations.hi.get_recommendations).toBe('अनुशंसाएँ प्राप्त करें');
  });

  it('has all required keys in both languages', () => {
    const requiredKeys = [
      'app_title', 'step1', 'step2', 'step3',
      'select_food', 'category', 'shelf_life_target',
      'get_recommendations', 'back', 'next', 'score',
      'disclaimer', 'analyzing',
    ];
    for (const key of requiredKeys) {
      expect(translations.en[key]).toBeDefined();
      expect(translations.hi[key]).toBeDefined();
    }
  });
});

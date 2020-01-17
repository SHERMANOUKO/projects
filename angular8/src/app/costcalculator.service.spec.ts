import { TestBed } from '@angular/core/testing';

import { CostcalculatorService } from './costcalculator.service';

describe('CostcalculatorService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CostcalculatorService = TestBed.get(CostcalculatorService);
    expect(service).toBeTruthy();
  });
});

import { TestBed, inject } from '@angular/core/testing';

import { StigService } from './stig.service';

describe('StigService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StigService]
    });
  });

  it('should be created', inject([StigService], (service: StigService) => {
    expect(service).toBeTruthy();
  }));
});

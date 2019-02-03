import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CciComponent } from './cci.component';

describe('CciComponent', () => {
  let component: CciComponent;
  let fixture: ComponentFixture<CciComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CciComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CciComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

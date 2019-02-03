import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StigsComponent } from './stigs.component';

describe('StigsComponent', () => {
  let component: StigsComponent;
  let fixture: ComponentFixture<StigsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StigsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StigsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

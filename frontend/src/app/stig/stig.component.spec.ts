import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StigComponent } from './stig.component';

describe('StigComponent', () => {
  let component: StigComponent;
  let fixture: ComponentFixture<StigComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StigComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CciTemplateComponent } from './cci-template.component';

describe('CciTemplateComponent', () => {
  let component: CciTemplateComponent;
  let fixture: ComponentFixture<CciTemplateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CciTemplateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CciTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

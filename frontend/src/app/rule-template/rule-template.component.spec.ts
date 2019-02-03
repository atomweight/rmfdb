import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RuleTemplateComponent } from './rule-template.component';

describe('RuleTemplateComponent', () => {
  let component: RuleTemplateComponent;
  let fixture: ComponentFixture<RuleTemplateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RuleTemplateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RuleTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

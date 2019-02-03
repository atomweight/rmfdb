import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RuleMetadataComponent } from './rule-metadata.component';

describe('RuleMetadataComponent', () => {
  let component: RuleMetadataComponent;
  let fixture: ComponentFixture<RuleMetadataComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RuleMetadataComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RuleMetadataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

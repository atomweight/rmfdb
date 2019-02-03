import { Component, OnInit, Input } from '@angular/core';

import { Rule } from '../models/stig';

@Component({
  selector: 'app-rule-template',
  templateUrl: './rule-template.component.html',
  styleUrls: ['./rule-template.component.css']
})
export class RuleTemplateComponent implements OnInit {

  @Input() rule: Rule;

  constructor() { }

  ngOnInit() {
  }

}

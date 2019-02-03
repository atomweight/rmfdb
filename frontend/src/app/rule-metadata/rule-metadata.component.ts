import { Component, OnInit, Input } from '@angular/core';

import { RuleMetadata } from '../models/stig';

@Component({
  selector: 'app-rule-metadata',
  templateUrl: './rule-metadata.component.html',
  styleUrls: ['./rule-metadata.component.css']
})
export class RuleMetadataComponent implements OnInit {

  @Input() metadata: RuleMetadata;

  constructor() { }

  ngOnInit() {
  }

}

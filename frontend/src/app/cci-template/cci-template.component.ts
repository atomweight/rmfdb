import { Component, OnInit, Input } from '@angular/core';

import { Cci } from '../models/control';

@Component({
  selector: 'app-cci-template',
  templateUrl: './cci-template.component.html',
  styleUrls: ['./cci-template.component.css']
})
export class CciTemplateComponent implements OnInit {

  @Input() cci: Cci;

  constructor() { }

  ngOnInit() {
  }

}

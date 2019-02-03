import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-timeago',
  templateUrl: './timeago.component.html',
  styleUrls: ['./timeago.component.css']
})
export class TimeagoComponent implements OnInit {

  @Input() dateInput: Date;

  constructor() { }

  ngOnInit() {
  }

}

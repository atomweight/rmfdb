import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';

import { AppService } from './services/app.service';
import { VersionResponse } from './models/app';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'rmfdb';
  version$: Observable<VersionResponse>;

  constructor(
    private appService: AppService,
  ) { }

  ngOnInit() {
    this.version$ = this.appService.getVersion();
  }
}

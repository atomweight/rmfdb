import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from "@angular/material";
import { tap } from 'rxjs/operators';

import { StigService } from '../services/stig.service';
import { StigsDataSource } from '../services/stigs.datasource';

@Component({
  selector: 'app-stigs',
  templateUrl: './stigs.component.html',
  styleUrls: ['./stigs.component.css']
})
export class StigsComponent implements OnInit {

  stigsDataSource: StigsDataSource;
  displayedColumns: string[] = ['name', 'version', 'release', 'release_date'];

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(
    private stigService: StigService
  ) { }

  ngOnInit() {
    this.stigsDataSource = new StigsDataSource(this.stigService);
    this.stigsDataSource.paginator = this.paginator;
    this.stigsDataSource.loadStigs();
  }

  ngAfterViewInit() {
    this.paginator.page
      .pipe(
        tap(() => this.loadStigsPage())
      )
    .subscribe();
  }

  loadStigsPage() {
    this.stigsDataSource.loadStigs(
      this.paginator.pageIndex,
      this.paginator.pageSize);
  }

}

import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from "@angular/material";
import { tap } from 'rxjs/operators';

import { ControlService } from '../services/control.service';
import { ControlsDataSource } from '../services/controls.datasource';

@Component({
  selector: 'app-controls',
  templateUrl: './controls.component.html',
  styleUrls: ['./controls.component.css']
})
export class ControlsComponent implements OnInit {

  controlsDataSource: ControlsDataSource;
  displayedColumns: string[] = ['control_id', 'name'];

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(
    private controlService: ControlService
  ) { }

  ngOnInit() {
    this.controlsDataSource = new ControlsDataSource(this.controlService);
    this.controlsDataSource.paginator = this.paginator;
    this.controlsDataSource.loadControls();
  }

  ngAfterViewInit() {
    this.paginator.page
      .pipe(
        tap(() => this.loadControlsPage())
      )
    .subscribe();
  }

  loadControlsPage() {
    this.controlsDataSource.loadControls(
      this.paginator.pageIndex,
      this.paginator.pageSize);
  }

}

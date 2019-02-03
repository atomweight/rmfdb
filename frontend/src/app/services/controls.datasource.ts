import { CollectionViewer, DataSource } from "@angular/cdk/collections";
import { MatPaginator } from "@angular/material";
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, finalize } from "rxjs/operators";

import { Control, ControlsResponse } from '../models/control';
import { ControlService } from './control.service';


export class ControlsDataSource extends DataSource<Control> {

    private controlSubject = new BehaviorSubject<Control[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);
    public loading$ = this.loadingSubject.asObservable();
    private _paginator: MatPaginator|null;

    constructor(
      private controlService: ControlService
    ) {
      super();
    }

    connect(collectionViewer: CollectionViewer): Observable<Control[]> {
        return this.controlSubject.asObservable();
    }

    disconnect(collectionViewer: CollectionViewer): void {
        this.controlSubject.complete();
        this.loadingSubject.complete();
    }

    loadControls(
      pageNum: number = 0,
      pageSize: number = 5
    ) {
        this.loadingSubject.next(true);
        this.controlService.getControls(
          pageNum,
          pageSize).pipe(
            catchError(() => of([])),
            finalize(() => this.loadingSubject.next(false))
        )
        .subscribe((controlsResponse: ControlsResponse) => {
          this.controlSubject.next(controlsResponse.controls);
          this._updatePaginator(controlsResponse.total);
        });
    }

    get paginator(): MatPaginator | null { return this._paginator; }

    set paginator(paginator: MatPaginator|null) {
      this._paginator = paginator;
    }

    _updatePaginator(filteredDataLength: number) {
      Promise.resolve().then(() => {
        if (!this.paginator) {
          return;
        }
        this.paginator.length = filteredDataLength;

        // If the page index is set beyond the page, reduce it to the last page.
        if (this.paginator.pageIndex > 0) {
          const lastPageIndex = Math.ceil(this.paginator.length / this.paginator.pageSize) - 1 || 0;
          this.paginator.pageIndex = Math.min(this.paginator.pageIndex, lastPageIndex);
        }
      });
    }
}

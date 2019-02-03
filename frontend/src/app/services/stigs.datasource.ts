import { CollectionViewer, DataSource } from "@angular/cdk/collections";
import { MatPaginator } from "@angular/material";
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, finalize } from "rxjs/operators";

import { Stig, StigsResponse } from '../models/stig';
import { StigService } from './stig.service';


export class StigsDataSource extends DataSource<Stig> {

    private stigSubject = new BehaviorSubject<Stig[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);
    public loading$ = this.loadingSubject.asObservable();
    private _paginator: MatPaginator|null;

    constructor(
      private stigService: StigService
    ) {
      super();
    }

    connect(collectionViewer: CollectionViewer): Observable<Stig[]> {
        return this.stigSubject.asObservable();
    }

    disconnect(collectionViewer: CollectionViewer): void {
        this.stigSubject.complete();
        this.loadingSubject.complete();
    }

    loadStigs(
      pageNum: number = 0,
      pageSize: number = 5
    ) {
        this.loadingSubject.next(true);
        this.stigService.getStigs(
          pageNum,
          pageSize).pipe(
            catchError(() => of([])),
            finalize(() => this.loadingSubject.next(false))
        )
        .subscribe((stigsResponse: StigsResponse) => {
          this.stigSubject.next(stigsResponse.stigs);
          this._updatePaginator(stigsResponse.total);
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

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { SearchResponse } from '../models/search';


@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private urn: string = '/api/search';

  constructor(
    private http: HttpClient
  ) { }

  search(
    query: string,
  ): Observable<SearchResponse> {
    return this.http.post<SearchResponse>(
        `${this.urn}`,
        {'query': query}
    );
  }

}

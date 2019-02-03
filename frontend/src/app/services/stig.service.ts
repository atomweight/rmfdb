import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Rule, Stig, StigsResponse } from '../models/stig';

@Injectable({
  providedIn: 'root'
})
export class StigService {
  private urn: string = '/api';

  constructor(
    private http: HttpClient
  ) { }

  getStigs(
    pageNum: number = 0,
    pageSize: number = 5
  ): Observable<StigsResponse> {
    let params = new HttpParams()
      .set('page', pageNum.toString())
      .set('pageSize', pageSize.toString())
    return this.http.get<StigsResponse>(`${this.urn}/stigs`, {params: params});
  }

  getStig(
    id: string,
  ): Observable<Stig> {
    return this.http.get<Stig>(`${this.urn}/stigs/${id}`);
  }

  getStigVersions(
    id: string,
  ): Observable<Stig[]> {
    return this.http.get<Stig[]>(`${this.urn}/stigs/${id}/versions`);
  }

  getRule(
    id: string,
  ): Observable<Rule> {
    return this.http.get<Rule>(`${this.urn}/rules/${id}`);
  }

  getRuleVersions(
    id: string,
  ): Observable<Rule[]> {
    return this.http.get<Rule[]>(`${this.urn}/rules/${id}/versions`);
  }

}



import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Cci, Control, ControlsResponse } from '../models/control';
import { Rule } from '../models/stig';


@Injectable({
  providedIn: 'root'
})
export class ControlService {
  private urn: string = '/api';

  constructor(
    private http: HttpClient
  ) { }

  getControls(
    pageNum: number = 0,
    pageSize: number = 5
  ): Observable<ControlsResponse> {
    let params = new HttpParams()
      .set('page', pageNum.toString())
      .set('pageSize', pageSize.toString())
    return this.http.get<ControlsResponse>(`${this.urn}/controls`, {params: params});
  }

  getControl(
    id: string,
  ): Observable<Control> {
    return this.http.get<Control>(`${this.urn}/controls/${id}`);
  }

  getCci(
    id: string,
  ): Observable<Cci> {
    return this.http.get<Cci>(`${this.urn}/ccis/${id}`);
  }

  getCciRules(
    id: string,
  ): Observable<Rule[]> {
    return this.http.get<Rule[]>(`${this.urn}/ccis/${id}/rules`);
  }

}



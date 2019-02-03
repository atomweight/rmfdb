import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { VersionResponse } from '../models/app';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  private urn: string = '/api';

  constructor(
	private http: HttpClient
  ) { }

  getVersion(): Observable<VersionResponse> {
	return this.http.get<VersionResponse>(`${this.urn}/version`);
  }
}

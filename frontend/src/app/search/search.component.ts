import { Component, OnInit, ViewChild } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { NavigationEnd, Router } from '@angular/router';
import { MatPaginator, MatTableDataSource } from '@angular/material';

import { SearchService } from '../services/search.service';
import { SearchResponse } from '../models/search';
import { Stig, Rule } from '../models/stig';
import { Cci, Control } from '../models/control';


@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  navigationSubscription;
  searchForm: FormGroup;
  hasSearched: boolean = false;
  searchResults: SearchResponse;
  stigsDisplayedColumns: string[] = ['name', 'version', 'release', 'release_date'];
  rulesDisplayedColumns: string[] = ['full_rule_id', 'rule_title', 'check_content', 'fix_text'];
  controlsDisplayedColumns: string[] = ['control_id', 'name', 'text', 'guidance'];
  ccisDisplayedColumns: string[] = ['cci_id', 'text', 'org_guidance', 'auditor_guidance'];
  stigsDataSource: MatTableDataSource<Stig>;
  rulesDataSource: MatTableDataSource<Rule>;
  controlsDataSource: MatTableDataSource<Control>;
  ccisDataSource: MatTableDataSource<Cci>;

  @ViewChild('stigsPaginator') stigsPaginator: MatPaginator;
  @ViewChild('rulesPaginator') rulesPaginator: MatPaginator;
  @ViewChild('controlsPaginator') controlsPaginator: MatPaginator;
  @ViewChild('ccisPaginator') ccisPaginator: MatPaginator;

  constructor(
    private fb: FormBuilder,
    private searchService: SearchService,
    private router: Router,
  ) {
    this.navigationSubscription = this.router.events.subscribe((e: any) => {
      if (e instanceof NavigationEnd) {
        this.ngOnInit();
      }
    });
  }

  ngOnInit() {
    this.hasSearched = false;
    this.searchForm = this.fb.group({
      'query': ['', [Validators.required, Validators.minLength(4)]],
    });
  }

  onSearch(): void {
    if (!this.searchForm.valid) return;
    this.searchResults = null;
    this.hasSearched = true;
    this.searchService.search(this.searchForm.get('query').value).subscribe(results => {
       this.searchResults = results;
       this.stigsDataSource = new MatTableDataSource(results.stigs);
       this.rulesDataSource = new MatTableDataSource(results.rules);
       this.controlsDataSource = new MatTableDataSource(results.controls);
       this.ccisDataSource = new MatTableDataSource(results.ccis);
       setTimeout(() => {
         this.stigsDataSource.paginator = this.stigsPaginator;
         this.rulesDataSource.paginator = this.rulesPaginator;
         this.controlsDataSource.paginator = this.controlsPaginator;
         this.ccisDataSource.paginator = this.ccisPaginator;
       });
    });
  }

  ngOnDestroy() {
    if (this.navigationSubscription) {
      this.navigationSubscription.unsubscribe();
    }
  }

}

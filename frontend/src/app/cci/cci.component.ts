import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Resolve, Router } from '@angular/router';
import { Observable } from 'rxjs';

import { ControlService } from '../services/control.service';
import { Cci } from '../models/control';
import { Rule } from '../models/stig';

@Component({
  selector: 'app-cci',
  templateUrl: './cci.component.html',
  styleUrls: ['./cci.component.css']
})
export class CciComponent implements OnInit {

  cci$: Observable<Cci>;
  cciRules$: Observable<Rule[]>;
  navigationSubscription;
  displayedColumns: string[] = ['full_rule_id', 'rule_title', 'stigs'];

  constructor(
    private controlService: ControlService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    this.navigationSubscription = this.router.events.subscribe((e: any) => {
      if (e instanceof NavigationEnd) {
        this.ngOnInit();
      }
    });
  }

  ngOnInit() {
    let id = this.route.snapshot.paramMap.get('id');
    let fullCciId = id.split('r')[0]
    this.cci$ = this.controlService.getCci(id);
    this.cciRules$ = this.controlService.getCciRules(fullCciId);
  }

  ngOnDestroy() {
    if (this.navigationSubscription) {
      this.navigationSubscription.unsubscribe();
    }
  }

}

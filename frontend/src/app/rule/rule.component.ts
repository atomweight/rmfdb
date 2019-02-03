import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Resolve, Router } from '@angular/router';
import { Observable } from 'rxjs';

import { StigService } from '../services/stig.service';
import { Rule } from '../models/stig';

@Component({
  selector: 'app-rule',
  templateUrl: './rule.component.html',
  styleUrls: ['./rule.component.css']
})
export class RuleComponent implements OnInit {

  rule$: Observable<Rule>;
  ruleVersions$: Observable<Rule[]>;
  navigationSubscription;

  constructor(
    private stigService: StigService,
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
    let fullRuleId = id.split('r')[0]
    this.rule$ = this.stigService.getRule(id);
    this.ruleVersions$ = this.stigService.getRuleVersions(fullRuleId);
  }

  ngOnDestroy() {
    if (this.navigationSubscription) {
      this.navigationSubscription.unsubscribe();
    }
  }

}

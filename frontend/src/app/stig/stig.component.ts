import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { Observable } from 'rxjs';

import { StigService } from '../services/stig.service';
import { Stig } from '../models/stig';

@Component({
  selector: 'app-stig',
  templateUrl: './stig.component.html',
  styleUrls: ['./stig.component.css']
})
export class StigComponent implements OnInit {

  stig$: Observable<Stig>;
  stigVersions$: Observable<Stig[]>;
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
    this.stig$ = this.stigService.getStig(id);
    this.stigVersions$ = this.stigService.getStigVersions(id);
  }

  ngOnDestroy() {
    if (this.navigationSubscription) {
      this.navigationSubscription.unsubscribe();
    }
  }

}

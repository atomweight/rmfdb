import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Resolve, Router } from '@angular/router';
import { Observable } from 'rxjs';

import { ControlService } from '../services/control.service';
import { Control } from '../models/control';

@Component({
  selector: 'app-control',
  templateUrl: './control.component.html',
  styleUrls: ['./control.component.css']
})
export class ControlComponent implements OnInit {

  control$: Observable<Control>;
  navigationSubscription;

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
    this.control$ = this.controlService.getControl(id);
  }

  ngOnDestroy() {
    if (this.navigationSubscription) {
      this.navigationSubscription.unsubscribe();
    }
  }

}

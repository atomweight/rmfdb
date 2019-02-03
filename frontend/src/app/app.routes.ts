import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { StigComponent } from './stig/stig.component';
import { RuleComponent } from './rule/rule.component';
import { ControlComponent } from './control/control.component';
import { CciComponent } from './cci/cci.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent,
    runGuardsAndResolvers: 'always'
  },
  {
    path: 'stigs/:id',
    component: StigComponent,
    runGuardsAndResolvers: 'paramsChange'
  },
  {
    path: 'rules/:id',
    component: RuleComponent,
    runGuardsAndResolvers: 'paramsChange'
  },
  {
    path: 'controls/:id',
    component: ControlComponent,
    runGuardsAndResolvers: 'paramsChange'
  },
  {
    path: 'ccis/:id',
    component: CciComponent,
    runGuardsAndResolvers: 'paramsChange'
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(
      routes,
      {
        enableTracing: false,
        onSameUrlNavigation: 'reload'
      })
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {}

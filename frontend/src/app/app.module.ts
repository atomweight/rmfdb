import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { FlexLayoutModule } from "@angular/flex-layout";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule,
         MatButtonModule,
         MatSidenavModule,
         MatIconModule,
         MatListModule,
         MatCardModule,
         MatInputModule,
         MatFormFieldModule,
         MatTableModule,
         MatPaginatorModule,
         MatSortModule,
         MatProgressSpinnerModule,
         MatChipsModule,
         MatTabsModule,
         MatBadgeModule,
         MatTooltipModule } from '@angular/material';
import { MomentModule } from 'ngx-moment';
import { TruncateModule } from 'ng2-truncate';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app.routes';
import { SearchComponent } from './search/search.component';
import { StigComponent } from './stig/stig.component';
import { TimeagoComponent } from './timeago/timeago.component';
import { RuleComponent } from './rule/rule.component';
import { RuleTemplateComponent } from './rule-template/rule-template.component';
import { RuleMetadataComponent } from './rule-metadata/rule-metadata.component';
import { StigsComponent } from './stigs/stigs.component';
import { ControlsComponent } from './controls/controls.component';
import { ControlComponent } from './control/control.component';
import { CciTemplateComponent } from './cci-template/cci-template.component';
import { CciComponent } from './cci/cci.component';

@NgModule({
  declarations: [
    AppComponent,
    SearchComponent,
    StigComponent,
    TimeagoComponent,
    RuleComponent,
    RuleTemplateComponent,
    RuleMetadataComponent,
    StigsComponent,
    ControlsComponent,
    ControlComponent,
    CciTemplateComponent,
    CciComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    FlexLayoutModule,
    BrowserAnimationsModule,
    LayoutModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatTabsModule,
    MatBadgeModule,
    MatTooltipModule,
    MomentModule,
    TruncateModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

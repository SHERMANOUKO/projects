import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from "@angular/material";
import { MatListModule } from '@angular/material/list';
import { HttpClientModule,HTTP_INTERCEPTORS } from '@angular/common/http';
import { Ng2CarouselamosModule } from 'ng2-carouselamos';
import { AgmCoreModule } from '@agm/core';
import { NgxPaginationModule } from 'ngx-pagination';
import 'hammerjs';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavComponent } from './nav/nav.component';
import { HomeComponent } from './home/home.component';
import { SupportComponent } from './support/support.component';
import { BillingComponent } from './billing/billing.component';
import { DeleteaccountComponent } from './deleteaccount/deleteaccount.component';
import { ViewprofileComponent } from './viewprofile/viewprofile.component';
import { EditprofileComponent } from './editprofile/editprofile.component';
import { EditpasswordComponent } from './editpassword/editpassword.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { LandingpageComponent } from './landingpage/landingpage.component';
import { LoginregisterComponent } from './loginregister/loginregister.component';
import { AddprofileComponent } from './addprofile/addprofile.component';
import { TokenInterceptorService } from '../app/tokeninterceptor.service';
import { ActivateComponent } from './activate/activate.component';
import { ContactusComponent } from './contactus/contactus.component';
import { FaqsComponent } from './faqs/faqs.component';
import { SearchComponent } from './search/search.component';
import { FiltersPipe } from './filters.pipe';
import { FindLandComponent } from './find-land/find-land.component';
import { SizepricelimitsComponent } from './sizepricelimits/sizepricelimits.component'

@NgModule({
  declarations: [
    AppComponent,
    NavComponent,
    HomeComponent,
    SupportComponent,
    BillingComponent,
    DeleteaccountComponent,
    ViewprofileComponent,
    EditprofileComponent,
    EditpasswordComponent,
    LoginComponent,
    RegisterComponent,
    LandingpageComponent,
    LoginregisterComponent,
    AddprofileComponent,
    ActivateComponent,
    ContactusComponent,
    FaqsComponent,
    SearchComponent,
    FiltersPipe,
    FindLandComponent,
    SizepricelimitsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    MatIconModule,
    MatListModule,
    HttpClientModule,
    Ng2CarouselamosModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIza... ',
      libraries: ['places']
    }),
    NgxPaginationModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptorService, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

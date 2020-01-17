import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SupportComponent } from './support/support.component';
import { DeleteaccountComponent } from './deleteaccount/deleteaccount.component';
import { EditpasswordComponent } from './editpassword/editpassword.component';
import { EditprofileComponent } from './editprofile/editprofile.component';
import { ViewprofileComponent } from './viewprofile/viewprofile.component';
import { LoginComponent } from "./login/login.component";
import { RegisterComponent } from "./register/register.component";
import { LandingpageComponent } from "./landingpage/landingpage.component";
import { AuthGuardService as AuthGuard } from "./guards/auth-guard.service";
import { ActivateComponent } from "./activate/activate.component";
import { ContactusComponent } from "./contactus/contactus.component"
import { FaqsComponent } from './faqs/faqs.component';
import { SearchComponent } from './search/search.component';
import { FindLandComponent } from './find-land/find-land.component';
import { SizepricelimitsComponent } from './sizepricelimits/sizepricelimits.component';

//  routerLink="/home"
const routes: Routes = [
  {path: 'home',component:HomeComponent,canActivate: [AuthGuard] },
  {path: 'support',component:SupportComponent,canActivate: [AuthGuard] },
  {path: 'deleteaccount',component:DeleteaccountComponent,canActivate: [AuthGuard] },
  {path: 'editpassword', component:EditpasswordComponent,canActivate: [AuthGuard] },
  {path: 'editprofile', component:EditprofileComponent,canActivate: [AuthGuard] },
  {path: 'viewprofile', component:ViewprofileComponent,canActivate: [AuthGuard] },
  {path : 'login' , component : LoginComponent},
  {path : 'register', component : RegisterComponent},
  {path : '', component : LandingpageComponent},
  {path : 'activate', component : ActivateComponent},
  {path : 'contactus', component : ContactusComponent},
  {path : 'faqs', component : FaqsComponent},
  {path : 'search', component : SearchComponent},
  {path: 'findland', component : FindLandComponent},
  {path: 'sizepricelimits', component : SizepricelimitsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

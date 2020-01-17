import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApidataService } from '../apidata.service'
import { FilemanagerService } from '../filemanager.service'

@Component({
  selector: 'app-addprofile',
  templateUrl: './addprofile.component.html',
  styleUrls: ['./addprofile.component.css']
})
export class AddprofileComponent implements OnInit {
  userType: string = localStorage.getItem('userType')
  userIdentifier: string = localStorage.getItem('userIdentifier')
  editProfileForm: FormGroup
  submitted:boolean = false
  show:boolean = false
  profileData: FormData;
  display: boolean = false
  displayCompany: boolean = false
  endPoint: string
  editProfileFormCompany: FormGroup
  success: boolean = null
  message: string

  constructor(private formBuilder:FormBuilder, private apidata:ApidataService, private filemanager: FilemanagerService) { }

  ngOnInit() {
    if(this.userType == 'individual'){
      this.display = true
      this.show = true
    }else if(this.userType == 'company'){
      this.show = true
      this.displayCompany = true
    }

    this.editProfileForm = this.formBuilder.group({
      phoneNumber: ['',Validators.pattern('[7][0-9]{8}')],
      county: ['',Validators.required],
      areaName: ['',Validators.required],
      postalAddress: ['',Validators.required],
      subcounty: ['',Validators.required],
      profilePhoto: ['',Validators.required],
      email: ['',Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')],
      aboutSeller: ['',Validators.required]
    })

    this.editProfileFormCompany = this.formBuilder.group({
      companySecondaryPhone: ['',Validators.pattern('[7][0-9]{8}')],
      companyTertiaryPhone: ['',Validators.pattern('[7][0-9]{8}')],
      companyHqCounty: ['',Validators.required],
      companyAddress: ['',Validators.required],
      companyFacebook: [''],
      companyInstagram: [''],
      companyTwitter: [''],
      companyProfilePhoto: ['',Validators.required],
      companySecondaryEmail: ['',Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')],
      aboutCompany: ['',Validators.required]
    })
  }

  get f() {return this.editProfileForm.controls}
  get fc() {return this.editProfileFormCompany.controls}

  onSelect(event, element: HTMLElement,){ 
    if( element.getAttribute('formControlName') === 'companyProfilePhoto'){
      this.filemanager.onChange(event, element.getAttribute('formControlName'),this.editProfileFormCompany)
    }else if( element.getAttribute('formControlName') === 'profilePhoto'){
      this.filemanager.onChange(event, element.getAttribute('formControlName'),this.editProfileForm)
    } 
  }

  onSubmit(){
    this.submitted = true
    this.endPoint = this.userType+'P'
    this.profileData = new FormData()

    if(this.userType === 'individual'){
      if(this.editProfileForm.invalid){
        return;
      }

      this.profileData.append('aboutIndividual' , this.editProfileForm.get('aboutSeller').value)
      this.profileData.append('individualAddress' , this.editProfileForm.get('postalAddress').value)
      this.profileData.append('individualArea' , this.editProfileForm.get('areaName').value)
      this.profileData.append('individualCounty' , this.editProfileForm.get('county').value)
      this.profileData.append('individualSecondaryEmail' , this.editProfileForm.get('email').value)
      this.profileData.append('individualSecondaryPhone' , this.editProfileForm.get('phoneNumber').value)
      this.profileData.append('individualSubCounty' , this.editProfileForm.get('subcounty').value)
      if(this.editProfileForm.get('profilePhoto').value !== null){
        this.profileData.append('front' , this.editProfileForm.get('profilePhoto').value)
      }
      this.profileData.append('individualIdNo',this.userIdentifier)

      this.apidata.postAuthDataFormData(this.profileData,this.endPoint).subscribe(
        (res)=>{
          console.log(res)         
          if(res.code === 200 ){
            this.message = "Profile successfuly created"
            this.success = true
          }else{
            this.message = res.message
            this.success = false
          }
        },
        (err)=>{
          console.log(err)
          this.message = "Fatal error: Unable to add. Try again and check your internet connection. If problem persists, contact support"
          this.success = false
        }
      )
    }else if (this.userType === 'company'){
      if(this.editProfileFormCompany.invalid){
        return;
      }
      
      this.endPoint = this.userType+'P'

      this.profileData.append('aboutCompany' , this.editProfileFormCompany.get('aboutCompany').value)
      this.profileData.append('companyAddress' , this.editProfileFormCompany.get('companyAddress').value)
      this.profileData.append('companyFacebook' , this.editProfileFormCompany.get('companyFacebook').value)
      this.profileData.append('companyHqCounty' , this.editProfileFormCompany.get('companyHqCounty').value)
      this.profileData.append('companySecondaryEmail' , this.editProfileFormCompany.get('companySecondaryEmail').value)
      this.profileData.append('companySecondaryPhone' , this.editProfileFormCompany.get('companySecondaryPhone').value)
      this.profileData.append('companyInstagram' , this.editProfileFormCompany.get('companyInstagram').value)
      this.profileData.append('companySecondaryPhone' , this.editProfileFormCompany.get('companySecondaryPhone').value)
      this.profileData.append('companyTertiaryPhone' , this.editProfileFormCompany.get('companyTertiaryPhone').value)
      this.profileData.append('companyTwitter' , this.editProfileFormCompany.get('companyTwitter').value)
      this.profileData.append('companyKraPin',this.userIdentifier)
      this.profileData.append('front' , this.editProfileFormCompany.get('companyProfilePhoto').value)


      alert(this.profileData)
      alert(this.editProfileFormCompany.get('companyProfilePhoto').value)
      alert(JSON.stringify(this.editProfileFormCompany.value))
      this.apidata.postAuthDataFormData(this.profileData,this.endPoint).subscribe(
        (res)=>{
          console.log(res)
          if(res.body.code === 200 ){
            this.message = "Profile successfuly created"
            this.success = true
          }else{
            this.message = "Unable to create profile"
            this.success = false
          }
        },
        (err)=>{
          console.log(err)
          this.message = "Fatal error: Unable to add. Try again and check your internet connection. If problem persists, contact support"
          this.success = false
        }
      )
    }
  }

}

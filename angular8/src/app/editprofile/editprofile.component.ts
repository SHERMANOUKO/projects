import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApidataService } from '../apidata.service'
import { FilemanagerService } from '../filemanager.service'

@Component({
  selector: 'app-editprofile',
  templateUrl: './editprofile.component.html',
  styleUrls: ['./editprofile.component.css']
})
export class EditprofileComponent implements OnInit {
  addProfile: boolean = true
  editProfile: boolean = false
  editAboutCompany: FormGroup
  about: boolean = null
  editSocialmediaCompany: FormGroup
  social: boolean = null
  editPrimaryCompany: FormGroup
  primary: boolean = null
  editSecondaryCompany: FormGroup
  secondary: boolean = null
  editAddressCompany: FormGroup
  address: boolean = null
  editAboutIndividual: FormGroup
  editPrimaryIndividual: FormGroup
  editSecondaryIndividual: FormGroup
  editAddressIndividual: FormGroup
  submitted:boolean = false
  userType: string = localStorage.getItem('userType')
  userIdentifier: string = localStorage.getItem('userIdentifier')
  message: string = null
  unavailableMessage: string = null
  isDataAvailable:boolean = false
  primaryMessage: string
  userData: Object
  returned: boolean = null
  
  constructor(private formBuilder:FormBuilder, private apidata:ApidataService, private filemanager: FilemanagerService) { }

  ngOnInit() {
    if(this.userType === 'individual'){
      this.editAboutIndividual = this.formBuilder.group({
        aboutIndividual:['',[Validators.required,Validators.maxLength(1000)]],
        individualIdNo:['']
      })
  
      this.editPrimaryIndividual = this.formBuilder.group({
        phoneNumber: ['',[Validators.required,Validators.pattern('[7][0-9]{8}')]],
        email: ['',[Validators.required,Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')]],
        individualIdNo:['']
      })
  
      this.editSecondaryIndividual = this.formBuilder.group({
        secondaryPhoneNumber:['',Validators.pattern('[7][0-9]{8}')],
        email: ['',Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')],
        individualIdNo:['']
      });
  
      this.editAddressIndividual = this.formBuilder.group({
        address: ['',Validators.required],
        county: ['',Validators.required],
        subCounty: ['',Validators.required],
        area: ['',Validators.required],
        individualIdNo:['']
      }); 
  
      this.editPrimaryIndividual.disable()
      this.editAboutIndividual.disable()
      this.editAddressIndividual.disable()
      this.editSecondaryIndividual.disable()

      this.apidata.getAuth(this.userType+'/'+this.userIdentifier).subscribe(
        (res)=>{
          console.log(res)
          if(res.code === 200){
            this.editPrimaryIndividual.patchValue({
             phoneNumber : res.data.sellerPhoneNo,
             email: res.data.sellerEmail
            });
          }else{
            this.primaryMessage = "Unable to retrieve primary contact info"
          }
        },
        (err)=>{
          this.primaryMessage = "Fatal! Unable to retrieve primary contact info"
        }
      )  

      this.apidata.getAuth(this.userType+'P/'+this.userIdentifier).subscribe(
        (res)=>{
          if(res.code === 401){
            this.message = "No info has been added yet"
            this.isDataAvailable = true
          }
          else if (res.code === 200){
            this.editAboutIndividual.patchValue({
              aboutIndividual: this.ifEmpty(res.data.aboutIndividual)
            });

            this.editSecondaryIndividual.patchValue({
              secondaryPhoneNumber: this.ifEmpty(res.data.individualSecondaryPhone),
              email: this.ifEmpty(res.data.individualSecondaryEmail),
            });

            this.editAddressIndividual.patchValue({
              address: this.ifEmpty(res.data.individualAddress),
              county: this.ifEmpty(res.data.individualCounty),
              subCounty: this.ifEmpty(res.data.individualSubCounty),
              area: this.ifEmpty(res.data.individualArea)
            });
          
            this.isDataAvailable = true
          }
          else{
            this.message = res.message
            this.isDataAvailable = true
          }
        },
        (err)=>{

        }
      )
    }  
    else if(this.userType === 'company'){
      this.editAboutCompany = this.formBuilder.group({
        aboutCompany:['',[Validators.required,Validators.maxLength(1000)]],
        individualIdNo:['']
      })
  
      this.editPrimaryCompany = this.formBuilder.group({
        phoneNumber: ['',[Validators.required,Validators.pattern('[7][0-9]{8}')]],
        email: ['',[Validators.required,Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')]],
        individualIdNo:['']
      })
  
      this.editSecondaryCompany = this.formBuilder.group({
        secondaryPhoneNumber:['',Validators.pattern('[7][0-9]{8}')],
        tertiaryPhoneNumber: ['',Validators.pattern('[7][0-9]{8}')],
        email: ['',Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')],
        individualIdNo:['']
      });
  
      this.editAddressCompany = this.formBuilder.group({
        companyAddress: ['',Validators.required],
        companyCounty: ['',Validators.required],
        individualIdNo:['']
      });
  
      this.editSocialmediaCompany = this.formBuilder.group({
        companyFacebook: [''],
        companyInstagram: [''],
        companyTwitter: [''],
        individualIdNo:['']
      }); 
  
      this.editPrimaryCompany.disable()
      this.editAboutCompany.disable()
      this.editAddressCompany.disable() 
      this.editSecondaryCompany.disable()
      this.editSocialmediaCompany.disable()

      this.apidata.getAuth(this.userType+'P/'+this.userIdentifier).subscribe(
        (res)=>{
          console.log(res)
          if(res.code === 401){
            this.unavailableMessage = "No info has been added yet"
            this.isDataAvailable = true
          }
          else if (res.code === 200){
            this.editAboutCompany.patchValue({
              aboutCompany: this.ifEmpty(res.data.aboutCompany)
            });

            // this.editPrimaryCompany.patchValue({
            //   : "ddsfdsf"
            // });

            this.editSecondaryCompany.patchValue({
              secondaryPhoneNumber: this.ifEmpty(res.data.companySecondaryPhone),
              tertiaryPhoneNumber: this.ifEmpty(res.data.companyTertiaryPhone),
              email: this.ifEmpty(res.data.companySecondaryEmail),
            });

            this.editAddressCompany.patchValue({
              companyAddress: this.ifEmpty(res.data.companyAddress),
              companyCounty: this.ifEmpty(res.data.companyHqCounty)
            });

            this.editSocialmediaCompany.patchValue({
              companyFacebook: this.ifEmpty(res.data.companyFacebook),
              companyInstagram: this.ifEmpty(res.data.companyInstagram),
              companyTwitter: this.ifEmpty(res.data.companyTwitter)
            });          
            this.isDataAvailable = true
          }
          else{
            this.message = res.message
            this.isDataAvailable = true
          }
        },
        (err)=>{

        }
      )
    }
  }
  // get fc() {return this.editProfileFormCompany.controls}
  
  ifEmpty(variable): string{
    if(variable === '' || variable === null){
      return 'No info added'
    }else{
      return variable
    }
  }

  showAddProfile(){
    this.addProfile = true
    this.editProfile = false
  }

  showEditProfile(){
    this.addProfile = false
    this.editProfile = true
  }

  activateAbout(){
    if(this.userType === 'company'){
      this.editAboutCompany.enable()
    }else if(this.userType === 'individual'){
      this.editAboutIndividual.enable()
    }
  }

  activatePrimary(){
    if(this.userType === 'company'){
      this.editPrimaryCompany.enable()
    }else if(this.userType === 'individual'){
      this.editPrimaryIndividual.enable()
    }
  }

  activateSecondary(){
    if(this.userType === 'company'){
      this.editSecondaryCompany.enable()
    }else if(this.userType === 'individual'){
      this.editSecondaryIndividual.enable()
    }
  }

  activateAddress(){
    if(this.userType === 'company'){
      this.editAddressCompany.enable()
    }else if(this.userType === 'individual'){
      this.editAddressIndividual.enable()
    }
  }

  activateSocial(){
    this.editSocialmediaCompany.enable()
  }

  submitAbout(){
    this.submitted = true
    this.about = true
    if(this.userType === 'individual'){
      if(this.editAboutIndividual.invalid){
        return;
      }

      this.editAboutIndividual.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editAboutIndividual.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
    else if(this.userType === 'company'){
      if(this.editAboutCompany.invalid){
        return;
      }

      this.editAboutIndividual.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editAboutCompany.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
  }
    
  submitPrimary(){
    this.submitted = true
    this.primary = true
    if(this.userType === 'individual'){
      if(this.editAboutIndividual.invalid){
        return;
      }

      this.editAboutIndividual.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editAboutIndividual.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
    else if(this.userType === 'company'){
      if(this.editAboutCompany.invalid){
        return;
      }

      this.editSecondaryCompany.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editSecondaryCompany.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
  }

  submitSecondary(){
    this.submitted = true
    this.secondary = true

    if(this.userType === 'individual'){
      if(this.editSecondaryIndividual.invalid){
        return;
      }

      this.editSecondaryIndividual.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editSecondaryIndividual.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
    else if(this.userType === 'company'){
      if(this.editSecondaryCompany.invalid){
        return;
      }

      this.editSecondaryCompany.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editSecondaryCompany.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
  }

  submitAddress(){
    this.submitted = true
    this.address = true

    if(this.userType === 'individual'){
      if(this.editAboutIndividual.invalid){
        return;
      }

      this.editAboutIndividual.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editAboutIndividual.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
    else if(this.userType === 'company'){
      if(this.editAboutCompany.invalid){
        return;
      }

      this.editAboutIndividual.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editAboutCompany.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
  }

  submitSocial(){
    this.submitted = true
    this.social = true

    if(this.userType === 'company'){
      if(this.editAboutCompany.invalid){
        return;
      }

      this.editAboutIndividual.patchValue({
        individualIdNo: this.userIdentifier
      });

      this.userData = this.editAboutCompany.value
      this.apiCall(this.userData,this.userType.charAt(0).toUpperCase() + this.userType.slice(1))
    }
  }

  apiCall(userData,userType){
    this.apidata.putAuthData(userData,'update'+userType+'Profile').subscribe(
      (res)=>{
        if(res.code === 200){
          console.log(res)
          this.message = res.message
          this.returned = true
        }
        else{
          console.log(res)
          this.message = res.message
          this.returned = false
        }
      },
      (err)=>{
        this.message = "Fatal error. Try again. If problem persists contact support. Ensure you have internet connection"
        this.returned = false
      }
    )
  }
}

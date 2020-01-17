import { Component, OnInit } from '@angular/core';
import { ApidataService } from '../apidata.service';

@Component({
  selector: 'app-viewprofile',
  templateUrl: './viewprofile.component.html',
  styleUrls: ['./viewprofile.component.css']
})
export class ViewprofileComponent implements OnInit {
  userType: string = localStorage.getItem('userType')
  userIdentifier: string = localStorage.getItem('userIdentifier')
  message: string = null
  isDataAvailable:boolean = false;
  aboutIndividual: string 
  individualAddress: string
  individualArea: string 
  individualCounty: string 
  individualSecondaryEmail: string 
  individualSubCounty: string 
  individualSecondaryPhone: string 
  aboutCompany: string
  companyAddress: string
  companyHqCounty: string
  companyInstagram: string
  companySecondaryPhone: string
  companySecondaryEmail: string
  companyTertiaryPhone: string
  companyTwitter: string
  companyFacebook: string

  constructor(private apidata: ApidataService) {}

  ngOnInit() {
    if(this.userType === 'individual'){
      this.apidata.getAuth(this.userType+'P/'+this.userIdentifier).subscribe(
        (res)=>{
          if(res.code === 401){
            this.message = "You havent added any profile information yet."
            this.aboutIndividual = "No About Info"
            this.individualAddress = "No Address Info"
            this.individualArea = "No Area Info"
            this.individualCounty = "No County Info"
            this.individualSecondaryEmail = "No Secondary Email Info"
            this.individualSubCounty = "No Subcounty Info"
            this.individualSecondaryPhone = "No Secondary Phone Info"
            this.isDataAvailable = true
            
          }else if(res.code === 200){
            this.aboutIndividual = this.ifEmpty(res.data.aboutIndividual)
            this.individualAddress = this.ifEmpty(res.data.individualAddress)
            this.individualArea = this.ifEmpty(res.data.individualArea)
            this.individualCounty = this.ifEmpty(res.data.individualCounty)
            this.individualSecondaryEmail = this.ifEmpty(res.data.individualSecondaryEmail)
            this.individualSubCounty = this.ifEmpty(res.data.individualSubCounty)
            this.individualSecondaryPhone = this.ifEmpty(res.data.individualSecondaryPhone)

            this.isDataAvailable = true
          }else{
            this.message = res.message
            this.isDataAvailable = true
          }
        },
        (err)=>{
          console.log(err.body)
        }
      )
      
    }
    else if(this.userType === 'company'){
      this.apidata.getAuth(this.userType+'P/'+this.userIdentifier).subscribe(
        (res)=>{
          if(res.code === 401){
            this.message = "You havent added any profile information yet."
            this.aboutCompany = "No About Info"
            this.companyAddress = "No Address Info"
            this.companyHqCounty = "No HQ Info"
            this.companyInstagram = "No Instagram Info"
            this.companySecondaryPhone = "No Secondary Phone Info"
            this.companySecondaryEmail = "No Secondary Email Info"
            this.companyTertiaryPhone = "No Tertiary Phone Info"
            this.companyTwitter = "No Twitter Info"
            this.companyFacebook = "No Facebook Info"
            this.isDataAvailable = true

          }else if(res.code === 200){
              this.aboutCompany = this.ifEmpty(res.data.aboutCompany)
              this.companyAddress = this.ifEmpty(res.data.companyAddress)
              this.companyHqCounty = this.ifEmpty(res.data.companyHqCounty)
              this.companyInstagram = this.ifEmpty(res.data.companyInstagram)
              this.companySecondaryPhone = this.ifEmpty(res.data.companySecondaryPhone)
              this.companyTertiaryPhone = this.ifEmpty(res.data.companyTertiaryPhone)
              this.companyTwitter = this.ifEmpty(res.data.companyTwitter)
              this.companyFacebook = this.ifEmpty(res.data.companyFacebook)
              alert(this.companyInstagram)
              this.isDataAvailable = true
          }else{
            this.message = res.message
            this.isDataAvailable = true
          }
        },
        (err)=>{
          console.log(err.body)
        }
      )
    }
  }

  ifEmpty(variable): string{
    if(variable === '' || variable === null){
      return 'No info added'
    }else{
      return variable
    }
  }

}

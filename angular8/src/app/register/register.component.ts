import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PasswordMatch } from '../validators/validate.validators';
import { ApidataService } from '../apidata.service';
import { FilemanagerService } from '../filemanager.service'

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  individualRegisterForm: FormGroup
  companyRegisterForm: FormGroup
  submitted; companySubmitted: boolean = false
  userData: FormData
  companyData: Object
  field: string
  response: Object
  error: Object
  show_individual : boolean = true
  show_company : boolean = false
  registerMessage: string
  succesful: boolean;


  constructor(private formBuilder:FormBuilder, private apidata: ApidataService, private filemanager: FilemanagerService) { }
  
  ngOnInit() {
    this.individualRegisterForm = this.formBuilder.group({
      inFullName: ['',Validators.required],
      inNationalID: ['',[Validators.required,Validators.pattern('[0-9]+'),Validators.minLength(8)]],
      inEmail: ['',[Validators.required,Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')]],
      inPhoneNumber: ['',[Validators.required,Validators.pattern('[7][0-9]{8}')]],
      inCounty: ['',Validators.required],
      inPassport: ['',Validators.required],
      inIdFront: ['',Validators.required],
      inIdBack: ['',Validators.required],
      inPassword: ['',[Validators.required,Validators.pattern('^[a-zA-Z0-9]{8,}')]],
      inConfirmPassword: ['',Validators.required]
    }
    ,{
      validator: PasswordMatch('inPassword','inConfirmPassword')
    })

    this.companyRegisterForm = this.formBuilder.group({
      companyName: ['',Validators.required],
      companyCeoName: ['',Validators.required],
      companyEmail: ['',[Validators.required,Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')]],
      companyPhoneNo: [null,[Validators.required,Validators.pattern('[0-9]{10}')]],
      companyRegistrationNo: [null,Validators.required],
      companyIncorporationYear: [null,[Validators.required,Validators.pattern('[1-2][0-9]{3}')]],
      companyKraPin: ['',Validators.required],
      userPassword: ['',[Validators.required,Validators.pattern('^[a-zA-Z0-9]{8,}')]],
      userConfirmPassword: ['',Validators.required]
    },{
      validator: PasswordMatch('userPassword','userConfirmPassword')
    })
  }
  
  get fi() {return this.individualRegisterForm.controls}
  get fc() {return this.companyRegisterForm.controls}

  onSelect(event, element: HTMLElement,){ 
    this.filemanager.onChange(event, element.getAttribute('formControlName'),this.individualRegisterForm)
  }

  onSubmitIndividual(){
    this.submitted = true;
    this.registerMessage = null
    this.succesful = null

    this.userData = new FormData()

    if(this.individualRegisterForm.invalid){ 
      return;
    }

    this.userData.append('sellerFullName', this.individualRegisterForm.get('inFullName').value);
    this.userData.append('sellerEmail', this.individualRegisterForm.get('inEmail').value);
    this.userData.append('sellerCounty', this.individualRegisterForm.get('inCounty').value);
    this.userData.append('sellerNationalIdNo', this.individualRegisterForm.get('inNationalID').value);
    this.userData.append('sellerPhoneNo', this.individualRegisterForm.get('inPhoneNumber').value);
    this.userData.append('userPassword', this.individualRegisterForm.get('inPassword').value);
    this.userData.append('back', this.individualRegisterForm.get('inIdBack').value);
    this.userData.append('front', this.individualRegisterForm.get('inIdFront').value);
    this.userData.append('pass', this.individualRegisterForm.get('inPassport').value);
    this.userData.append('userType','individual');
    this.userData.append('sellerVerification','unverified');


    this.apidata.postUnauthData(this.userData,'auth/createIndividual').subscribe(
      (res) => {
        if(res.code === 200){
          this.succesful = true
          this.registerMessage = res.message
        }else{
          this.succesful = false
          this.registerMessage = res.message
        }
      },
      (err) => {
        this.succesful = false
        this.registerMessage = err.message
      }
    );
   }
  
  onSubmitCompany(){
    this.companySubmitted = true;
    this.registerMessage = null
    this.succesful = null
    
    if(this.companyRegisterForm.invalid){
      return;
    }

    this.companyData = {
      "companyName": this.companyRegisterForm.get('companyName').value,
      "companyCeoName": this.companyRegisterForm.get('companyCeoName').value,
      'companyEmail': this.companyRegisterForm.get('companyEmail').value,
      'companyPhoneNo': parseInt(this.companyRegisterForm.get('companyPhoneNo').value),
      'companyRegistrationNo': this.companyRegisterForm.get('companyRegistrationNo').value,
      'companyIncorporationYear': parseInt(this.companyRegisterForm.get('companyIncorporationYear').value),
      'companyKraPin': this.companyRegisterForm.get('companyKraPin').value,
      'userPassword': this.companyRegisterForm.get('userPassword').value,
      'userType': 'company',   
    }

    this.apidata.postUnauthData(this.companyData,'auth/createCompany').subscribe(
      (res)=>{
        if(res.code === 200){
          this.succesful = true
          this.registerMessage = res.message
        }else{
          this.succesful = false
          this.registerMessage = res.message
        }
      },
      (err)=>{
        this.succesful = false
        this.registerMessage = err.message
      }
    )

  }

  toggle() {
    this.show_individual = !this.show_individual;
    this.show_company = !this.show_company;
  }
  resume() {
    this.show_company = false;
    this.show_individual = true;
  }
}

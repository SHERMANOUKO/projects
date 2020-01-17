import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { PasswordMatch } from '../validators/validate.validators';
import { ApidataService } from '../apidata.service';

@Component({
  selector: 'app-editpassword',
  templateUrl: './editpassword.component.html',
  styleUrls: ['./editpassword.component.css']
})
export class EditpasswordComponent implements OnInit {
  editPasswordForm: FormGroup;
  submitted: boolean = false;
  userType: string = localStorage.getItem('userType')
  userIdentifier: string = localStorage.getItem('userIdentifier')
  email: string
  set:boolean = null
  message: string = null
  load: boolean = false
  spin: boolean = false

  constructor(private formBuilder:FormBuilder, private apidata:ApidataService) { }

  ngOnInit() {
    this.apidata.getAuth(this.userType+'/'+this.userIdentifier).subscribe(
      (res)=>{
        if(res.code === 200){
          if(this.userType === 'company'){
            this.email = res.data.companyEmail
          }
          else if(this.userType === 'individual'){
            this.email = res.data.sellerEmail
            this.load = true
          }
        }else{
          this.set = false
          this.message = res.message
          this.load = true
        }
      },
      (err)=>{
       this.set = false
       this.message = "Fatal! Email not retrieved. Try again and ensure you have good internet connectivity"
        this.load = true
      }
    )  

    this.editPasswordForm = this.formBuilder.group({
      userOldPassword: ['',Validators.required],
      userNewPassword: ['',[Validators.required, Validators.minLength(8),Validators.pattern('.*[a-zA-Z0-9]')]],
      confirmPassword: ['',Validators.required],
      userEmail:['']
    },{
      validator: PasswordMatch('userNewPassword','confirmPassword')
    })
  }

  get f() {return this.editPasswordForm.controls;}

  onSubmit(){
    this.message = null
    this.submitted=true
    if(this.editPasswordForm.invalid){
      return;
    }
    this.editPasswordForm.patchValue({
      userEmail: this.email 
    });
    this.spin = true
    this.apidata.putAuthData(this.editPasswordForm.value,'updatePassword').subscribe(
      (res)=>{
        this.spin = false
        this.set = true
        this.message = res.message
      },
      (err)=>{
        this.spin = false
        this.message = "Fatal! Unable to update password. Try again and ensure you have good internet connectivity"
        this.set = false
      }
    )
    this.spin = false
  }
}
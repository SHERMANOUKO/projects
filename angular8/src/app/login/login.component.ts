import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../authentication.service'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup
  submitted: boolean = false
  error: Object;
  response: boolean = true
  x: number;

  constructor(private formBuilder:FormBuilder, private authservice: AuthenticationService) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      userEmail : ['',Validators.required],
      userPassword : ['',Validators.required]
    })
  }

  get f() {return this.loginForm.controls}

  onSubmit(){
    this.submitted = true;
 
    if(this.loginForm.invalid){
      return;
    }
    this.authservice.login(this.loginForm.value).subscribe(
      (res) => {
        this.response = res.state
      },
      (err) => {
        this.error = err
        console.log(err)
      }
    );

  }

}


import { Component, OnInit} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApidataService } from '../apidata.service';
import { Support } from '../securities';

@Component({
  selector: 'app-support',
  templateUrl: './support.component.html',
  styleUrls: ['./support.component.css']
})

export class SupportComponent implements OnInit {
  contactForm: FormGroup
  submitted: boolean = false
  contactData: Object
  response: Support
  error: Object
  succesful: number = null
  message: string

  constructor(private formBuilder: FormBuilder, private apidata: ApidataService) { }

  ngOnInit() {
    this.contactForm = this.formBuilder.group({
      messageSenderIdentifier: [localStorage.getItem('userIdentifier')],
      messageMessage: ['',[Validators.required,Validators.maxLength(500)]]
    })
  }

  get f(){ return this.contactForm.controls; }

  onSubmit(){
    this.submitted = true;
    
    //stop execution if form is invalid
    if(this.contactForm.invalid){
      return;
    }

    this.apidata.postAuthData(this.contactForm.value,'message').subscribe(
      (res)=>{
        this.response = res
        if(this.response.code == 200){
          this.succesful = 1
          alert("dsdsds")
        }else{
          this.succesful = 0
          this.message = this.response.message
        }
      },
      (err) =>{
        this.succesful = 2
      }
    )
  }
}

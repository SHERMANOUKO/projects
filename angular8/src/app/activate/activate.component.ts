import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute} from '@angular/router';
import { FormBuilder, FormGroup , Validators} from '@angular/forms';
import { ApidataService } from '../apidata.service'

@Component({
  selector: 'app-activate',
  templateUrl: './activate.component.html',
  styleUrls: ['./activate.component.css']
})
export class ActivateComponent implements OnInit {
  key; email; message: string = null
  activateForm: FormGroup
  submitted; activated: boolean = false

  constructor(
    private route:ActivatedRoute, 
    private router:Router, 
    private formBuilder:FormBuilder, 
    private apiService:ApidataService
  ) { }

  ngOnInit() {
    this.key = this.route.snapshot.queryParamMap.get('key');
    this.email = this.route.snapshot.queryParamMap.get('email');

    if(!this.key || !this.email){
      this.router.navigate( ['login']);
    }

    this.activateForm = this.formBuilder.group({
      key: [this.key],
      code: ['',[Validators.required,Validators.pattern('[a-zA-Z0-9]{6}')]]
    })
  }

  get f(){return this.activateForm.controls}
  onSubmit(){
    this.submitted = true
    this.message = null
    this.activated = false

    if(this.activateForm.invalid){
      return
    }

    console.log(this.activateForm.value)
    this.apiService.postUnauthData(this.activateForm.value,'/auth/selfVerifyUser').subscribe(
      (res)=>{
        alert("done")
        if(res.code === 200){
          this.activated = true
        }else{
          this.message = res.message
        }
      },
      (err)=>{
        this.message = err
      }
    )
    
  }
}

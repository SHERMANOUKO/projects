import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../authentication.service'
import { ApidataService } from '../apidata.service';
import { Validators, FormGroup, FormBuilder } from '@angular/forms';
import { FilemanagerService } from '../filemanager.service';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})


export class NavComponent implements OnInit {
  showContent: boolean
  userIdentifier: string = localStorage.getItem('userIdentifier')
  userType:string = localStorage.getItem('userType')
  photo:boolean = null
  appTitle: string = 'plotsApp';
  message: string
  imageBlobUrl; profilePicture: any
  url: string
  load: boolean = false
  editImageForm: FormGroup
  submitted: boolean
  imageData: FormData
  update: string = null
  reloadPage: boolean = null
  dataspin: boolean = false
  altImg: string = "/assets/images/profile.jpeg"

  constructor(private auth: AuthenticationService, private filemanager:FilemanagerService, private apidata:ApidataService, private formBuilder:FormBuilder) { }
  
  ngOnInit() {
      this.loadPic()

      this.editImageForm = this.formBuilder.group({
        file: ['',Validators.required],
      })
  }

  loadPic(){
    this.apidata.getAuth(this.userType+'P/'+this.userIdentifier).subscribe(
      (res)=>{
        if(res.code === 401){
          this.photo = false
          this.message = "No profile photo found."
          this.load = true
        }else if(res.code === 200){
          this.url = 'closedSinglePhoto/download/31970205/selleridentity/profile.jpeg'
          this.apidata.getImages(this.url).subscribe((res)=>{
            console.log(res)
            this.imageBlobUrl = this.createImageFromBlob(res)
          },
          (err)=>{
          })
          this.photo = true
        }else{
          this.photo = false
          this.message = res.message 
          this.load = true
        }
      },
      (err)=>{
        this.load = true
        this.photo = false
        this.message = "Unable to load profile picture. Kindly refresh page"
      }
    )
  }

  get f(){return this.editImageForm.controls}

  onSelect(myFile, element: HTMLElement,){ 
    if(myFile.length > 0){
      if(myFile[0].size > 5120000){
        this.f.file.setErrors({limitSize: true})
      }else{
        this.profilePicture = myFile[0]
      }
    }
  }


  createImageFromBlob(image: Blob){
    let reader = new FileReader();    
    reader.addEventListener("loadend", () => {
      this.imageBlobUrl = reader.result;
      this.load = true
    }, false);

    if(image){
      reader.readAsDataURL(image)
    }
  }

  onSubmit(){
    this.submitted = true
    this.imageData = new FormData()
    
    if(this.editImageForm.invalid){
      return
    }
    this.imageData.append('file',this.profilePicture)

    this.userType = this.userType.charAt(0).toUpperCase() + this.userType.slice(1)

    this.dataspin = true

    this.apidata.putAuthData(this.imageData,'update'+this.userType+'ProfilePhoto/'+this.userIdentifier).subscribe(
      (res)=>{
        if(res.code === 200){
          this.dataspin = false
          this.update = res.message
          this.reloadPage = true
        }
        else{
          this.dataspin = false
          this.update = res.message
        }
      },
      (err)=>{
        this.dataspin = false
        this.update = "Fatal error. Try again. If problem persists contact support. Ensure you have internet connection" 
      }
    )
    this.dataspin = false
  }
  reload(){
    if(this.reloadPage){
      window.location.reload();
    }
  }

  logOut(){
    this.auth.logout()
  }

}

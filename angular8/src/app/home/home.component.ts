import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { ApidataService } from '../apidata.service'
import { FilemanagerService } from '../filemanager.service'
import { LatitudeCheck, LongitudeCheck, SizeCheck } from '../validators/validate.validators';
import { tap, map} from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {
  asyncProperties : Observable<Object[]>; 
  properties; propertiesInfo; promotionInfo; promotions : any[]
  addPropertyForm; promotePropertyForm: FormGroup
  submitted; show; showMap; loading; promotion; promoting: boolean = false
  propertyData: FormData;
  response; error: Object
  headers: string[];
  url; message; propertyMessage; promotionMessage; promotionType; promotionReply: string;
  showLands: boolean = true
  fileone; filetwo; selectedPromotion: any = null
  successful; promotionWait; promotionSuccess: boolean = null
  lat; lng; totalCount; promotionId: number
  zoom: number = 15;
  display; confirmPromotion; promotionSelected: string = 'none'
  pageNo: number = 0
  p: number = 1
  

  userIdentifier: string = localStorage.getItem('userIdentifier')

  constructor(private formBuilder: FormBuilder, private apidata: ApidataService, private filemanager: FilemanagerService) {}

  ngOnInit() {
    this.loading = true;
    this.apidata.getAuth('singlePropertyCount?ownerIdentifier='+this.userIdentifier).subscribe(
      (res)=>{
        if(res.code === 200){
          this.totalCount = res.data
          this.getPromotions()
          this.getPage(1);
        }
      },
      (err)=>{
        
      }
    )

    this.addPropertyForm = this.formBuilder.group({
      propertyAreaName: ['',Validators.required],
      propertyCounty: ['',Validators.required],
      propertyLatitude: ['',Validators.required],
      propertyLongitude: ['',Validators.required],
      propertySize: ['',Validators.required],
      propertyTitleDeedNo: ['',Validators.required],
      propertyLandAliasName: ['',Validators.required],
      propertystartingPrice: ['',[Validators.required,Validators.pattern('[0-9]+\.[0-9]+')]],
      propertyDescription: ['',[Validators.required,Validators.maxLength(500)]],
      landone: ['',Validators.required],
      landtwo: ['',Validators.required]
    },
    {
      validators: [
        LatitudeCheck('propertyLatitude'),
        LongitudeCheck('propertyLongitude'),
        SizeCheck('propertySize')
      ]
    })

    this.promotePropertyForm = this.formBuilder.group({
      phoneNumber: ['',[Validators.required,Validators.pattern('[7][0-9]{8}')]],
      transactioCode: ['',Validators.required],
      promotionId:[''],
      propertyId: ['']
    })
  }

  get f(){return this.addPropertyForm.controls}
  get fp(){return this.promotePropertyForm.controls}

  getPromotions(){
    this.apidata.getAuth('normalPromotionUser/'+localStorage.getItem('userType')).subscribe(
      (res)=>{
        if(res.code === 200){
          this.promotions = res.data
        }else{
          this.promotionMessage = res.message
        }
      },
      (err)=>{
        this.promotionMessage = 'Fatal! Error (Promotions)'
      }
    )
  }

  getPage(page: number) {
    this.loading = true;
    this.pageNo = page - 1
    this.asyncProperties = this.apidata.getAuth('singleProperty?number='+this.pageNo+'&size=6&ownerIdentifier='+this.userIdentifier)
      .pipe(
        tap<any>(res=>{
          if(res.code === 200){
            this.p = page;
            this.loading = false;
          }else{
            this.propertyMessage = res.message
            this.loading = false;
          }
        }),
        map<any,any>(res => res.data)
    )
  }

  checkPromotions(propertyId,promotionId){
    this.apidata.getAuth('/normalPromotionViablityStatus/'+propertyId+'/'+promotionId).subscribe(
      (res)=>{
        if(res.code === 200){
          if(res.data){
            this.promotePropertyForm.patchValue({
              promotionId: promotionId,
              propertyId: propertyId,
            });
            this.promoting = true
            this.promotionSelected = 'none'
            this.confirmPromotion = 'block'
          }else if(!res.data){
            this.promoting = true
            this.promotionSelected = 'none'
            this.confirmPromotion = 'block'
            this.promotionMessage = "This land has an active promotion for that promotion type"
          }
        }else{
          this.promoting = true
          this.promotionSelected = 'none'
          this.confirmPromotion = 'block'
          this.promotionMessage = "Promotions cannot not be completed at this time. Try again later"
        }
      },
      (err)=>{
        this.promoting = true
        this.promotionSelected = 'none'
        this.confirmPromotion = 'block'
        this.promotionMessage = 'Fatal! Error (Promotions)'
      }
    )
  }

  promote(promotionInfo){
    this.promotionInfo = promotionInfo
    this.show = false
    this.showLands = false
    this.promotion = true
  }

  showDetails(property){
    this.propertiesInfo = property
    this.display="block"; 
  
  }

  onCloseHandled(){
    this.display='none'; 
    this.confirmPromotion = 'none'
    this.selectedPromotion = 'none'
    this.promotionMessage = null
    this.promotionWait = null
    this.promotionSuccess = null
    this.promotionReply = null
  }
  
  viewMap(latitude,longitude){
    this.promotion = false
    this.show = false
    this.showLands = false
    this.showMap = true
    this.lat = latitude
    this.lng = longitude
  }

  removeMap(){
    this.loading = true;
    this.promotion = false
    this.show = false
    this.showLands = true
    this.showMap = false
    this.promotionId = null
  }

  replaceSpecial(stringValue){
    let newStringValue = stringValue.replace(/[^\w\s]/gi, '');
    return newStringValue
  }

  selectPromotion(args) {
    this.promotionId = args
    this.selectedPromotion = this.promotions.find(i => i.promotionId == this.promotionId);
  }

  confirmPromotionModal(identifier){
    if(this.selectedPromotion == null){
      this.promotionSelected = 'block'
    }else if(this.selectedPromotion.promotionId == null){
      this.promotionSelected = 'block'
    }else{
      this.checkPromotions(identifier,this.selectedPromotion.promotionId)
    }
  }

  onSelect(myFile, element: HTMLElement,){ 
    if(myFile.length > 0){
      if(element.getAttribute('formControlName') === 'landone'){
        if(myFile[0].size > 5120000){
          this.f.landone.setErrors({limitSize: true})
        }else{
          this.fileone = myFile[0]
        }
      }
      else if(element.getAttribute('formControlName') === 'landtwo'){
        if(myFile[0].size > 5120000){
          this.f.landtwo.setErrors({limitSize: true})
        }else{
          this.filetwo = myFile[0]
        }
      }
    }
  }

  showForm(){
    this.show = true
    this.showLands = false
  }

  hideForm(){
    this.show = false
    this.showLands = true
  }

  onSubmit(){
    this.submitted = true
    
    this.propertyData = new FormData()
  
    if(this.addPropertyForm.invalid){
      return
    }

    this.propertyData.append('propertyAreaName',this.addPropertyForm.get('propertyAreaName').value)
    this.propertyData.append('propertyCounty',this.addPropertyForm.get('propertyCounty').value)
    this.propertyData.append('propertyLatitude',this.addPropertyForm.get('propertyLatitude').value)
    this.propertyData.append('propertyLongitude',this.addPropertyForm.get('propertyLongitude').value)
    this.propertyData.append('propertyTitleDeedNo',this.addPropertyForm.get('propertyTitleDeedNo').value)
    this.propertyData.append('propertyLandAliasName',this.addPropertyForm.get('propertyLandAliasName').value)
    this.propertyData.append('propertystartingPrice',this.addPropertyForm.get('propertystartingPrice').value)
    this.propertyData.append('propertyDescription',this.addPropertyForm.get('propertyDescription').value)
    this.propertyData.append('landOne',this.fileone)
    this.propertyData.append('landtwo',this.filetwo)
    this.propertyData.append('propertySize',this.addPropertyForm.get('propertySize').value)
    this.propertyData.append('propertyOwner',localStorage.getItem('userType'))
    this.propertyData.append('propertyOwnerIdentifier',localStorage.getItem('userIdentifier'))
    this.propertyData.append('propertyIdentifier',this.replaceSpecial(this.addPropertyForm.get('propertyTitleDeedNo').value))
  

    this.apidata.postAuthData(this.propertyData,'property').subscribe(
      (res)=>{
        if(res.code === 200){
          this.message = res.message
          this.successful = true
        }else{
          this.message = res.message
          this.successful = false
        }
      },
      (err)=>{
        this.message = "Fatal error! Retry. Ensure you have internet connection. If problem persists, contact support"
        this.successful = false
      }
    )
  }

  onPromote(){
    this.submitted = true
    this.promotionWait = true

    if(this.promotePropertyForm.invalid){
      this.promotionWait = false
      return
    }

    this.apidata.postAuthData(this.promotePropertyForm.value,'promoteProperty').subscribe(
      (res)=>{
        if(res.code === 200){
          this.promotionWait = false
          this.promotionReply = res.message
          this.promotionSuccess = true
        }else{
          this.promotionWait = false
          this.promotionReply = res.message
          this.promotionSuccess = false
        }
      },
      (err)=>{
        this.promotionWait = false
        this.promotionReply = err.message
        this.promotionSuccess = false
      }
    )
  }
}

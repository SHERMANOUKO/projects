import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApidataService } from '../apidata.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';
import { CostcalculatorService } from '../costcalculator.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  latitude: number; longitude: number; pageSize: number; upperLimit: number
  searchData: any; singlePropertyData: Object
  propertyData : Observable<Object[]>; 
  paymentForm: FormGroup
  message: any; sellerID: string
  filterCounty: string = null
  filterSellerType: string = null
  filterLandUse: string = null
  filterSize: number = null 
  filterPrice: number = null
  found: boolean; singleProperty: boolean; showPhoneModal: boolean; greenCardModal: boolean; loading: boolean; submitted: boolean; available: boolean = null
  displayPhone: string; displayGreenCard: string = 'none'
  displayAllProperty: string; displayFilters: string = 'block'
  pageNo: number; greenCardAmount: number
  p: number = 1
  countyIcon: boolean = true
  sizeIcon: boolean = true
  priceIcon: boolean = true
  landUseIcon: boolean = true
  sellerTypeIcon: boolean = true
  loadingGreenCard: boolean;
  greenCardMessage: string;


  constructor(
    private formBuilder:FormBuilder,
    private activatedRoute: ActivatedRoute, 
    private router:Router, 
    private apiservice:ApidataService,
    private costCalculatorService:CostcalculatorService
    ) { 
    this.activatedRoute.queryParams.subscribe((params: { [x: string]: any; }) => {
      if(params["search"] === 'true'){
        this.latitude = Number(params["latitude"]);
        this.longitude = Number(params["longitude"]);
        this.upperLimit = Number(params["upperLimit"]);
      }else{
        this.router.navigate([""]);  
      }
      
    });
  
  }

  ngOnInit() {
    this.pageNo = 1
    this.pageSize = 3
    this.getPage(this.pageNo)

    this.paymentForm =  this.formBuilder.group({
      phoneNumber:['',[Validators.required,Validators.pattern('[7][0-9]{8}')]],
      email: ['',[Validators.required,Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,5}$')]]
    })
  }

  greenCard(price: any){
    this.loadingGreenCard =  true
    this.greenCardModal = true
    this.displayGreenCard = 'block'
    this.costCalculatorService.greenCardCost(price).subscribe(
      (res)=>{
        if(res.code === 200){
          this.greenCardAmount = res.data
          this.loadingGreenCard =  false
        }else{
          this.greenCardMessage = res.message
          this.loadingGreenCard =  false
        }
      },
      (err)=>{
        this.greenCardMessage = err.message
        this.loadingGreenCard =  false
      }
    )
  }

  get f() {return this.paymentForm.controls}

  onSubmit(){
    this.submitted = true

    if(this.paymentForm.invalid){
      return
    }

    console.log(this.paymentForm.value)
  }

  checkCheckBoxvalue(filter){
    if(filter.landUse)
      if(filter.landUse === 'all')
        this.filterLandUse = null
      else
        this.filterLandUse = filter.landUse
    
    if(filter.maxPrice)
      this.filterPrice = filter.maxPrice
    
    if(filter.sellerType)
      if(filter.sellerType === 'both')
        this.filterSellerType = null
      else
        this.filterSellerType = filter.sellerType
    
    if(filter.county)
      if(filter.county === 'all')
        this.filterCounty = null
      else
        this.filterCounty = filter.county
    
    if(filter.maxSize)
      this.filterSize = filter.maxSize

    console.log({
      maxPrice: this.filterPrice,
      maxSize: this.filterSize,
      county: this.filterCounty,
      sellerType: this.filterSellerType,
      landUse: this.filterLandUse
    })

  }

  infoModal(property: Object){
    this.singlePropertyData = property
    this.displayFilters = 'none'
    this.displayAllProperty = 'none'
    this.singleProperty = true
  }

  backToSearch(){
    this.singleProperty = false
    this.displayAllProperty = 'block'
    this.displayFilters = 'block'
  }

  phoneModal(sellerID: string){
    this.sellerID = sellerID
    this.displayPhone = 'block'
    this.showPhoneModal = true
  }

  onCloseHandled(){
    this.showPhoneModal = false
    this.greenCardMessage = null
    this.displayPhone = 'none'
    this.displayGreenCard = 'none'
  }

  toggleIcon(icon: string){
    if(icon === 'county'){
      if(this.countyIcon === true){
        this.countyIcon = false
      }else{
        this.countyIcon = true
      }
    }else if(icon === 'size'){
      if(this.sizeIcon === true){
        this.sizeIcon = false
      }else{
        this.sizeIcon = true
      }
    }else if(icon === 'price'){
      if(this.priceIcon === true){
        this.priceIcon = false
      }else{
        this.priceIcon = true
      }
    }else if(icon === 'sellerType'){
      if(this.sellerTypeIcon === true){
        this.sellerTypeIcon = false
      }else{
        this.sellerTypeIcon = true
      }
    }else if(icon === 'landUse'){
      if(this.landUseIcon === true){
        this.landUseIcon = false
      }else{
        this.landUseIcon = true
      }
    }
  }

  getPage(page: number) {
    this.displayAllProperty = 'none'
    this.loading = true;
    this.pageNo = page - 1
    this.propertyData = this.apiservice.postUnauthData(
      {
        "latitude": this.latitude,
        "longitude": this.longitude,
        "pageNumber": this.pageNo,
        "pageSize": this.pageSize,
        "upperLimit": this.upperLimit
      },
      'openPropertySearchByLocation')
      .pipe(
        tap<any>(res=>{
          if(res.code === 200){
            this.p = page;
            this.loading = false;
            this.available = true
            this.displayAllProperty = 'block'
          }else{
            this.available = false
            this.found = true
            this.message = res.message
            this.loading = false;
            this.displayAllProperty = 'block'
          }
        },
        err=>{
          this.available = false
          this.found = true
          this.loading = false;
          this.message = err.message
          this.displayAllProperty = 'block'
        }),
        map<any,any>(res => res.data)
    )
  }
}

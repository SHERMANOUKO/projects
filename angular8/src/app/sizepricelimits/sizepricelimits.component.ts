import { Component, OnInit } from '@angular/core';
import {Router, ActivatedRoute } from '@angular/router'
import { ApidataService } from '../apidata.service'
import { CostcalculatorService } from '../costcalculator.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';

@Component({
  selector: 'app-sizepricelimits',
  templateUrl: './sizepricelimits.component.html',
  styleUrls: ['./sizepricelimits.component.css']
})
export class SizepricelimitsComponent implements OnInit {
  pageSize: number;
  singlePropertyData: Object
  propertyData : Observable<Object[]>; 
  paymentForm: FormGroup
  filterLandUse: string = null
  filterCounty: string = null
  message: any; sellerID: string
  found: boolean; singleProperty: boolean; showPhoneModal: boolean; greenCardModal: boolean; loading: boolean; submitted: boolean; available: boolean = null
  displayPhone: string; displayGreenCard: string = 'none'
  displayAllProperty: string; displayFilters: string = 'block'
  pageNo: number; greenCardAmount: number
  p: number = 1
  countyIcon: boolean = true
  landUseIcon: boolean = true
  loadingGreenCard: boolean;
  greenCardMessage: string;
  maximum: number
  minimum: number
  field: string

  constructor(
    private formBuilder:FormBuilder,
    private activatedRoute: ActivatedRoute, 
    private router:Router, 
    private apiservice:ApidataService,
    private costCalculatorService:CostcalculatorService
    
  ) {
    this.activatedRoute.queryParams.subscribe((params: { [x: string]: any; })=>{
      if(params["search"] === 'true'){
        this.minimum = params["minimum"]
        this.maximum = params["maximum"]
        this.field = params["field"]
      }else{
        this.router.navigate([""]);  
      }
    })
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
    
    if(filter.county)
      if(filter.county === 'all')
        this.filterCounty = null
      else
        this.filterCounty = filter.county
    

    console.log({
      maxPrice: this.filterLandUse,
      county: this.filterCounty,
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
        "maximum": this.maximum,
        "minimum": this.minimum,
        "pageNumber": this.pageNo,
        "pageSize": this.pageSize,
        "field": this.field
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

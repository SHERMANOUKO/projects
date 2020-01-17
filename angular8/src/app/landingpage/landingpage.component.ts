import { Component, OnInit, ElementRef, NgZone, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApidataService } from '../apidata.service';
import { MapsAPILoader } from '@agm/core';
import { NavigationExtras, Router } from '@angular/router';

@Component({
  selector: 'app-landingpage',
  templateUrl: './landingpage.component.html',
  styleUrls: ['./landingpage.component.css']
})

export class LandingpageComponent implements OnInit {
  latitude; longitude: number
  findLandForm: FormGroup
  items; sectionOne: Array<any> = []
  companies: Array<any> = []
  individuals: Array<any> = []
  logos: Array<any> = []
  displayEmail; displayPhone; displayMap: string = 'none'
  removeMap: string = 'block'
  showEmailModal; showPhoneModal; invalidSearch; submitted: boolean = false
  lat; lng; totalCount: number
  zoom: number = 15;

  @ViewChild("search", {static: false})
  searchElementRef: ElementRef;

  constructor(
    private mapsAPILoader: MapsAPILoader, 
    private ngZone: NgZone, 
    private apiservice:ApidataService,
    private formBuilder: FormBuilder,
    private router:Router
  ) {
    // this.apiservice.getUnauth('openPropertyPromoted').subscribe(
    //   (res)=>{
    //     alert("yeeey")
    //     if(res.code === 200){
    //       this.items = res.data
    //     }else{
    //       this.items = null
    //     }
    //   },
    //   (err)=>{
    //     this.items = null
    //   }
    // )

    // this.apiservice.getUnauth('openPropertyPromoted').subscribe(
    //   (res)=>{
    //     alert("yeeey")
    //     if(res.code === 200){
    //       this.companies = res.data
    //     }else{
    //       this.companies = null
    //     }
    //   },
    //   (err)=>{
    //     this.companies = null
    //   }
    // )

    // this.apiservice.getUnauth('openPropertyPromoted').subscribe(
    //   (res)=>{
    //     alert("yeeey")
    //     if(res.code === 200){
    //       this.individuals = res.data
    //     }else{
    //       this.individuals = null
    //     }
    //   },
    //   (err)=>{
    //     this.individuals = null
    //   }
    // )

    this.individuals = [
      { name: 'assets/images/1.jpeg' },
      { name: 'assets/images/2.jpg' },
      { name: 'assets/images/3.jpg' },
      { name: 'assets/images/4.jpeg' },
      { name: 'assets/images/5.jpeg' },
      { name: 'assets/images/6.jpg' },
      { name: 'assets/images/7.jpg' },
      { name: 'assets/images/8.jpg' },
      { name: 'assets/images/9.jpg' },
    ]

    this.companies = [
      { name: 'assets/images/1.jpeg' },
      { name: 'assets/images/2.jpg' },
      { name: 'assets/images/3.jpg' },
      { name: 'assets/images/4.jpeg' },
      { name: 'assets/images/5.jpeg' },
      { name: 'assets/images/6.jpg' },
      { name: 'assets/images/7.jpg' },
      { name: 'assets/images/8.jpg' },
      { name: 'assets/images/9.jpg' },
    ]

    this.items = [
      { name: 'assets/images/1.jpeg' },
      { name: 'assets/images/2.jpg' },
      { name: 'assets/images/3.jpg' },
      { name: 'assets/images/4.jpeg' },
      { name: 'assets/images/5.jpeg' },
      { name: 'assets/images/6.jpg' },
      { name: 'assets/images/7.jpg' },
      { name: 'assets/images/8.jpg' },
      { name: 'assets/images/9.jpg' },
    ]

    this.logos = [
      { name: 'assets/images/logo1.png' },
      { name: 'assets/images/logo2.png' },
      { name: 'assets/images/logo3.png' },
      { name: 'assets/images/logo4.jpeg' },
      { name: 'assets/images/logo5.jpeg' },
      { name: 'assets/images/logo6.png' },
      { name: 'assets/images/logo7.png' },
      { name: 'assets/images/logo8.png' },
      { name: 'assets/images/logo9.png' },
      { name: 'assets/images/logo10.jpeg' },
      { name: 'assets/images/logo11.png' },
      { name: 'assets/images/logo12.jpeg' }
    ]
  }

  ngOnInit() {
    this.findLandForm = this.formBuilder.group({
      county: ['',Validators.required],
      maxArea: ['',Validators.pattern('[0-9]+')],
      minArea: ['',Validators.pattern('[0-9]+')],
      maxPrice: ['',Validators.pattern('[0-9]+')],
      minPrice: ['',Validators.pattern('[0-9]+')],
      sellerType: ['',Validators.required]
    })

    this.mapsAPILoader.load().then(() => {
      let autocomplete = new google.maps.places.Autocomplete(this.searchElementRef.nativeElement,{});
      autocomplete.addListener("place_changed", () => {
        this.ngZone.run(() => {
          //get the place result
          let place: google.maps.places.PlaceResult = autocomplete.getPlace();

          //verify result
          if (place.geometry === undefined || place.geometry === null) {
            return;
          }

          //set latitude, longitude 
          this.latitude = place.geometry.location.lat();
          this.longitude = place.geometry.location.lng();
        });
      });
    });
  }

  get f() { return this.findLandForm.controls}

  onTap(){
    alert("yeeeeyy")
  }

  searchLocation(radius){
    this.invalidSearch = false
    if(!this.latitude || !this.longitude || !radius){
      this.invalidSearch = true
      return
    }  
    
    let navigationExtras: NavigationExtras = {
      queryParams: {
          "search":true,
          "latitude": this.latitude,
          "longitude": this.longitude,
          "upperLimit": radius
        }
    };

    this.router.navigate(["search"], navigationExtras);  
  }

  filterLand(){
    this.submitted = true

    if(this.findLandForm.invalid){
      return
    }

    // if(this.findLandForm.get())
    if(!this.findLandForm.get('maxArea').value){
      this.findLandForm.controls['maxArea'].patchValue(100000000000000000000);
    }
    if(!this.findLandForm.get('minArea').value){
      this.findLandForm.controls['minArea'].patchValue(0);
    }
    if(!this.findLandForm.get('minPrice').value){
      this.findLandForm.controls['minPrice'].patchValue(0);
    }
    if(!this.findLandForm.get('maxPrice').value){
      this.findLandForm.controls['maxPrice'].patchValue(100000000000000000000);
    }
    
    let navigationExtras: NavigationExtras = {
      queryParams: {
        search: true,
        details: JSON.stringify(this.findLandForm.value)
      }
    }

    this.router.navigate(["findland"], navigationExtras); 
  }

  emailModal(){
    this.showEmailModal = true
    this.displayEmail = 'block'
  }

  phoneModal(){
    this.showPhoneModal = true
    this.displayPhone = 'block'
  }

  onCloseHandled(){
    this.showPhoneModal = false
    this.displayPhone = 'none'
    this.showEmailModal = false
    this.displayEmail = 'none'
  }

  viewMap(){
    this.lat = -1.1634727
    this.lng = 37.081282999999985
    this.removeMap = 'none'
    this.displayMap = 'block'
  }

  hideMap(){
    this.removeMap = 'block'
    this.displayMap = 'none'
  }

  findLimits(minimum,maximum,field){
    let navigationExtras: NavigationExtras = {
      queryParams: {
          "search":true,
          "minimum": minimum,
          "maximum": maximum,
          "field":field
        }
    };

    this.router.navigate(["sizepricelimits"], navigationExtras);  
  }
}

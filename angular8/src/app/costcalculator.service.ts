import { Injectable } from '@angular/core';
import { ApidataService } from './apidata.service';

@Injectable({
  providedIn: 'root'
})
export class CostcalculatorService {

  constructor(private apiservice:ApidataService) { }

  greenCardCost(price){
    return this.apiservice.getUnauth('/greenCardPrice?price='+price)
  }
}

import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpEvent, HttpHandler, HttpRequest } from '@angular/common/http';
import {Observable} from "rxjs";
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor {

  constructor(private router:Router) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let date: Date = new Date()
    date.setTime(date.getTime()+(date.getTimezoneOffset()*60*1000)+10800000)
    let expiry = new Date(localStorage.getItem('expiresAt'))
    
    if (req.headers.get('No-Auth-Needed') == "True")
      return next.handle(req.clone());
   
    if(!expiry){
        this.router.navigate(['login']);
        return   
    }else if(expiry < date){
        this.router.navigate(['login']);
        return
    }
    
    let tokenizedReq = req.clone({
      setHeaders: {
        Authorization: 'Bearer ' + localStorage.getItem('accessToken')
      }
    })
    return next.handle(tokenizedReq)
  }
}

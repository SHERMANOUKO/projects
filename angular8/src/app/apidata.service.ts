import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ApidataService {
  apiUrl: string = 'http://xx.xxx.xxx.xx:9000/'

  constructor(private httpClient:HttpClient) { }
  headers = new HttpHeaders({'No-Auth-Needed':'True'});
  // httpParams: 

// params = new HttpParams()
//   .set('page', PageNo)
//   .set('sort', SortOn);
    
  postUnauthData(data,apiEndPoint){
    return this.httpClient.post<any>(this.apiUrl+apiEndPoint,data,{headers: this.headers});
  }

  postAuthData(data,apiEndPoint){
    return this.httpClient.post<any>(this.apiUrl+apiEndPoint,data)
  }

  putAuthData(data,apiEndPoint){
    return this.httpClient.put<any>(this.apiUrl+apiEndPoint,data)
  }

  postAuthDataFormData(data,apiEndPoint){
    return this.httpClient.post<any>(this.apiUrl+apiEndPoint,data)
  }

  getAuth(apiEndPoint){
    return this.httpClient.get<any>(this.apiUrl+apiEndPoint)
  }

  getUnauth(apiEndPoint){
    return this.httpClient.get<any>(this.apiUrl+apiEndPoint,{headers: this.headers})
  }

  getImages(apiEndPoint):Observable<Blob>{
    return this.httpClient.get(this.apiUrl+apiEndPoint,{responseType: "blob"})
  }
}


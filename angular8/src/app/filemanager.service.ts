import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FilemanagerService {
  field: string

  constructor() { }

public onChange(event, formControlName, form) {
  this.field =  formControlName
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      form.get(this.field).setValue(file);
    }
  }
}

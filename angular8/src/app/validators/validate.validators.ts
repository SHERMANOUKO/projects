import { FormGroup } from '@angular/forms';

export function PasswordMatch(controlName: string, matchingControlName: string){
    return(formGroup: FormGroup)=>{
        const control = formGroup.controls[controlName];
        const matchingControl = formGroup.controls[matchingControlName]

        if (matchingControl.errors && !matchingControl.errors.mustMatch) {
            return;
        }

        if(control.value !== matchingControl.value){
            matchingControl.setErrors({ passwordMatch: true})
        }else{
            matchingControl.setErrors(null)
        }
    }
}

export function LatitudeCheck(controlName: string){
    return(formGroup: FormGroup)=>{
        const control = formGroup.controls[controlName];
        const check = Math.abs(control.value)

        if (control.errors) {
            return;
        }

        if(check  && check <= 90 || check === 0){
            control.setErrors(null)
        }else{
            control.setErrors({ latitudeCheck: true})
        }
    }
}

export function LongitudeCheck(controlName: string){
    return(formGroup: FormGroup)=>{
        const control = formGroup.controls[controlName];
        const check = Math.abs(control.value)

        if (control.errors) {
            return;
        }

        if(check  && check <= 180 || check === 0){
            control.setErrors(null)
        }else{
            control.setErrors({ longitudeCheck: true})
        }
    }
}

export function SizeCheck(controlName: string){
    return(formGroup: FormGroup)=>{
        const control = formGroup.controls[controlName];
         
        if (control.errors) {
            return;
        }

        if(isNaN(Number(control.value))){
            control.setErrors({ sizeCheck: true})
        }else{
            control.setErrors(null) 
        }
    }
}
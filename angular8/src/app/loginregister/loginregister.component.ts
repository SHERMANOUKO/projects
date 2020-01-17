import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-loginregister',
  templateUrl: './loginregister.component.html',
  styleUrls: ['./loginregister.component.css']
})
export class LoginregisterComponent implements OnInit {
  state: boolean = true

  constructor() { }

  ngOnInit() {}

  toggleIcon(state){
    this.state = state
  }

}

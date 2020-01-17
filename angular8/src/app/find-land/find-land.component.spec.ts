import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FindLandComponent } from './find-land.component';

describe('FindLandComponent', () => {
  let component: FindLandComponent;
  let fixture: ComponentFixture<FindLandComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FindLandComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FindLandComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

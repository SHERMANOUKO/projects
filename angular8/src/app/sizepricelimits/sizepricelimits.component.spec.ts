import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SizepricelimitsComponent } from './sizepricelimits.component';

describe('SizepricelimitsComponent', () => {
  let component: SizepricelimitsComponent;
  let fixture: ComponentFixture<SizepricelimitsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SizepricelimitsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SizepricelimitsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

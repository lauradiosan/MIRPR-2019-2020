import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { FooterComponent } from "./footer.component";
import { By } from "@angular/platform-browser";

describe("FooterComponent", () => {
  let component: FooterComponent;
  let fixture: ComponentFixture<FooterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [FooterComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FooterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });

  it("should render copyrights", () => {
    const rights = fixture.debugElement.query(By.css("#rights"));
    expect(rights.nativeElement.textContent).not.toBeNull();
  });
});

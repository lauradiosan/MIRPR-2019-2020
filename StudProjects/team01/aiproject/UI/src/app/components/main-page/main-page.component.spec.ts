import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { MainPageComponent } from "./main-page.component";
import { By } from "@angular/platform-browser";
import { MainPageModule } from "./main-page.module";
import { AppRoutingModule } from "src/app/app-routing.module";
import { PagesModule } from "src/app/pages.module";

describe("MainPageComponent", () => {
  let component: MainPageComponent;
  let fixture: ComponentFixture<MainPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [MainPageModule, AppRoutingModule, PagesModule]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MainPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });

  it("should render header", () => {
    const header = fixture.debugElement.query(By.css("#header"));
    expect(header).not.toBeNull();
  });

  it("should render footer", () => {
    const footer = fixture.debugElement.query(By.css("#footer"));
    expect(footer).not.toBeNull();
  });

  it("should render body", () => {
    const body = fixture.debugElement.query(By.css("#bodyContainer"));
    expect(body).not.toBeNull();
  });
});

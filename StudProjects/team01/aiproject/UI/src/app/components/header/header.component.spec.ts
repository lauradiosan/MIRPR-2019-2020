import { async, ComponentFixture, TestBed } from "@angular/core/testing";
import { By } from "@angular/platform-browser";
import { HeaderComponent } from "./header.component";

describe("HeaderComponent", () => {
  let component: HeaderComponent;
  let fixture: ComponentFixture<HeaderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HeaderComponent]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });

  it("should render title", () => {
    component.title = "Title";
    fixture.detectChanges();
    const title = fixture.debugElement.query(By.css("#title"));
    expect(title.nativeElement.textContent).toEqual("Title");
  });

  it("should render logo", () => {
    const logo = fixture.debugElement.query(By.css("#logo"));
    expect(logo).not.toBeNull();
  });
});

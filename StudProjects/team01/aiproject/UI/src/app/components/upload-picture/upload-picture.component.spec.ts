import { async, ComponentFixture, TestBed } from "@angular/core/testing";

import { UploadPictureComponent } from "./upload-picture.component";
import { By } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";

describe("UploadPictureComponent", () => {
  let component: UploadPictureComponent;
  let fixture: ComponentFixture<UploadPictureComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [UploadPictureComponent],
      imports: [FormsModule]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UploadPictureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });

  it("should render input file", () => {
    const input = fixture.debugElement.query(By.css("#fileInput"));
    expect(input).not.toBeNull();
  });

  it("should render radio boxex", () => {
    const boxMalformation = fixture.debugElement.query(
      By.css("#is-malformation")
    );
    const boxNotMalformation = fixture.debugElement.query(
      By.css("#no-malformation")
    );
    expect(boxMalformation.attributes.value).toEqual("malformation");
    expect(boxNotMalformation.attributes.value).toEqual("no-malformation");
  });

  it("should call fileChosen", () => {
    spyOn(component, "fileChosen");
    const input = fixture.debugElement.query(By.css("#fileInput"));
    input.triggerEventHandler("change", {});
    expect(component.fileChosen).toHaveBeenCalled();
  });

  it("should change name", () => {
    component.fileChosen({ target: { value: "\\name.pic" } });
    expect(component.fileName).toEqual("name.pic");
  });

  it("should submit form", () => {
    spyOn(component, "submit");
    const form = fixture.debugElement.query(By.css("#picForm"));
    form.triggerEventHandler("submit", {});
    expect(component.submit).toHaveBeenCalled();
  });
});

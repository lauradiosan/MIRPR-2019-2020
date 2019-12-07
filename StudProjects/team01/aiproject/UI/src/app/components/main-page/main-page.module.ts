import { MainPageComponent } from "./main-page.component";
import { HeaderComponent } from "../header/header.component";
import { NgModule } from "@angular/core";
import { AppRoutingModule } from "src/app/app-routing.module";
import { FooterComponent } from "../footer/footer.component";
import { UploadPictureComponent } from "../upload-picture/upload-picture.component";
import { PagesModule } from "src/app/pages.module";

@NgModule({
  declarations: [MainPageComponent, HeaderComponent, FooterComponent],
  imports: [AppRoutingModule, PagesModule],
  providers: [],
  bootstrap: [MainPageComponent],
  exports: [MainPageComponent, HeaderComponent, FooterComponent]
})
export class MainPageModule {}

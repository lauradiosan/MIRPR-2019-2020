import { NgModule } from "@angular/core";
import { PageNotFoundComponent } from "./components/page-not-found/page-not-found.component";
import { UploadPictureComponent } from "./components/upload-picture/upload-picture.component";
import { FormsModule } from "@angular/forms";
import { ViewerComponent } from './components/viewer/viewer.component';

@NgModule({
  declarations: [PageNotFoundComponent, UploadPictureComponent, ViewerComponent],
  imports: [FormsModule],
  providers: [],
  exports: [PageNotFoundComponent, UploadPictureComponent]
})
export class PagesModule {}

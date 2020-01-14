import {NgModule} from '@angular/core';
import {PageNotFoundComponent} from './components/page-not-found/page-not-found.component';
import {UploadPictureComponent} from './components/upload-picture/upload-picture.component';
import {FormsModule} from '@angular/forms';
import {ViewerComponent} from './components/viewer/viewer.component';
import {CommonModule} from '@angular/common';
import {MatProgressSpinnerModule} from '@angular/material';

@NgModule({
  declarations: [PageNotFoundComponent, UploadPictureComponent, ViewerComponent],
  imports: [FormsModule, CommonModule, MatProgressSpinnerModule],
  providers: [],
  exports: [PageNotFoundComponent, UploadPictureComponent]
})
export class PagesModule {
}

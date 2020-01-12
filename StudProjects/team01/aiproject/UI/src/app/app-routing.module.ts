import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { UploadPictureComponent } from "./components/upload-picture/upload-picture.component";
import { PageNotFoundComponent } from "./components/page-not-found/page-not-found.component";
import { ViewerComponent } from "./components/viewer/viewer.component";

const routes: Routes = [
  { path: "", component: UploadPictureComponent },
  { path: "viewer", component: ViewerComponent },
  { path: "**", component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

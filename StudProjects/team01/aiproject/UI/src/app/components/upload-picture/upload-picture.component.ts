import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {base64StringToBlob} from 'blob-util';

@Component({
  selector: 'app-upload-picture',
  templateUrl: './upload-picture.component.html',
  styleUrls: ['./upload-picture.component.css']
})
export class UploadPictureComponent implements OnInit {
  fileName: string;
  file;
  labels = ['DCM', 'HCM', 'NOR', 'RV', 'MINF'];
  isLoading = false;

  constructor(private router: Router) {
  }

  ngOnInit() {
  }

  submit(event) {
    const formData = new FormData(event.target);
    this.isLoading = true;
    fetch('http://172.30.118.59:5000/process-image', {
      method: 'POST',
      headers: {Accept: 'application/json'},
      body: formData
    }).then(response =>
      response.json()
    )
      .then(response => {
        this.isLoading = false;
        this.router.navigate(['/viewer'],
          {state: {image: base64StringToBlob(response.file, 'image/gif'), message: response.message}});
      }).catch(err => {
      console.error(err);
      this.isLoading = false;
      alert(err);
    });
  }

  fileChosen(e) {
    this.file = e.target.value;
    const pathSplit: Array<string> = e.target.value.split('\\');
    this.fileName = pathSplit[pathSplit.length - 1];
  }
}

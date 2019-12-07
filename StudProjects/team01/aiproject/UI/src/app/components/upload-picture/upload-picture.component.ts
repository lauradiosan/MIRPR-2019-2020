import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {resolveFileWithPostfixes} from '@angular/compiler-cli/ngcc/src/utils';

@Component({
  selector: 'app-upload-picture',
  templateUrl: './upload-picture.component.html',
  styleUrls: ['./upload-picture.component.css']
})
export class UploadPictureComponent implements OnInit {
  fileName: string;
  file;

  constructor(private router: Router) {
  }

  ngOnInit() {
  }

  submit(event) {
    const formData = new FormData(event.target);
    fetch('http://localhost:5000/process-image', {
      method: 'POST',
      headers: {Accept: 'application/json'},
      body: formData
    }).then(response => response.json())
      .then(response => {
        this.router.navigate(['/viewer', {context: JSON.stringify(response)}]);
      }).catch(err => {
      console.error(err);
    });
  }

  fileChosen(e) {
    this.file = e.target.value;
    const pathSplit: Array<string> = e.target.value.split('\\');
    this.fileName = pathSplit[pathSplit.length - 1];
  }
}

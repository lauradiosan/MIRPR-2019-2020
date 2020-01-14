import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-viewer',
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.css']
})
export class ViewerComponent implements OnInit {
  message: string;
  image;
  constructor() {
  }

  ngOnInit() {
    this.readImage(window.history.state.image);
    this.message = window.history.state.message;
  }

  readImage(img: Blob) {
    const reader = new FileReader();
    reader.addEventListener('load', () => {
      this.image = reader.result;
    });
    if (img) {
      reader.readAsDataURL(img);
    }
  }
}

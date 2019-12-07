import { Component, OnInit, Input } from "@angular/core";

@Component({
  selector: "app-main-page",
  templateUrl: "./main-page.component.html",
  styleUrls: ["./main-page.component.css"]
})
export class MainPageComponent implements OnInit {
  title: string = "Cor meum";
  constructor() {}

  ngOnInit() {}
}

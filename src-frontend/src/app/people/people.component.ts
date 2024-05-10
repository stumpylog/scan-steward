import { Component, OnInit } from '@angular/core';
import { PeopleService } from './people.service';

@Component({
  selector: 'app-people',
  standalone: true,
  imports: [],
  templateUrl: './people.component.html',
  styleUrl: './people.component.css',
})
export class PeopleComponent implements OnInit {
  constructor(private peopleService: PeopleService) {}

  ngOnInit(): void {}

  getPeople() {
    return this.peopleService.getPeople();
  }
}

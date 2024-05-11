import { Component, OnInit } from '@angular/core';
import { PeopleService } from '../api/services';
import { PersonReadSchema, PagedPersonReadSchema } from '../api/models';
import { HttpErrorResponse } from '@angular/common/http';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-people',
  standalone: true,
  imports: [RouterLink, RouterOutlet],
  templateUrl: './people.component.html',
  styleUrl: './people.component.css',
})
export class PeopleComponent implements OnInit {
  people: PersonReadSchema[] = [];

  constructor(private peopleService: PeopleService) {}

  ngOnInit(): void {
    this.getPeople();
  }

  getPeople() {
    this.peopleService.getPeople().subscribe({
      next: (response: PagedPersonReadSchema) => {
        this.people = response.items;
      },
      error: (e: HttpErrorResponse) => {
        console.error(e);
      },
      complete: () => {
        console.info('complete');
      },
    });
  }
}

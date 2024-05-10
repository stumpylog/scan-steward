import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class PeopleService {
  people = [
    { id: 1, name: 'Test Name', description: 'This is a description' },
    { id: 2, name: 'Another Name' },
  ];

  constructor() {}

  getPeople() {
    return this.people.slice();
  }
}

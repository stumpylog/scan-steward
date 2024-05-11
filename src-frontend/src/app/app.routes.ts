import { Routes } from '@angular/router';
import { PeopleComponent } from './people/people.component';
import { PersonCreateComponent } from './people/person-create/person-create.component';
import { PersonViewComponent } from './people/person-view/person-view.component';
import { PersonEditComponent } from './people/person-edit/person-edit.component';

export const routes: Routes = [
  {
    path: 'people',
    component: PeopleComponent,
    children: [
      {
        path: 'new',
        component: PersonCreateComponent,
      },
      {
        path: ':id',
        component: PersonViewComponent,
      },
      {
        path: ':id/edit',
        component: PersonEditComponent,
      },
    ],
  },
];

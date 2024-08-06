import { NgModule } from "@angular/core";
import { RouterModule, type Routes } from "@angular/router";
import { DashboardComponent } from "./dashboard/dashboard/dashboard.component";
import { PeopleListComponent } from "./people/people-list/people-list.component";
import { PhotoWallComponent } from "./photos/photo-wall/photo-wall.component";

const routes: Routes = [
	{
		path: "",
		component: DashboardComponent,
	},
	{
		path: "photos",
		component: PhotoWallComponent,
	},
	{
		path: "people",
		component: PeopleListComponent,
	},
	// {
	//   path: 'locations',
	//   component: LocationListComponent
	// },
	// {
	//   path: 'dates',
	//   component: DateListComponent
	// },
	// {
	//   path: 'profile',
	//   component: ProfileComponent
	// }
];

@NgModule({
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule],
})
export class AppRoutingModule {}

import { provideHttpClient } from "@angular/common/http";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { BrowserModule } from "@angular/platform-browser";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { DashboardComponent } from "./dashboard/dashboard/dashboard.component";
import { NavigationComponent } from "./navigation/navigation.component";
import { PeopleListComponent } from "./people/people-list/people-list.component";
import { PersonCreateComponent } from "./people/person-create/person-create.component";
import { PersonEditComponent } from "./people/person-edit/person-edit.component";
import { PhotoWallComponent } from "./photos/photo-wall/photo-wall.component";

@NgModule({
	declarations: [
		AppComponent,
		NavigationComponent,
		PeopleListComponent,
		PersonCreateComponent,
		PersonEditComponent,
		DashboardComponent,
		PhotoWallComponent,
	],
	imports: [
		// Angular
		BrowserModule,
		FormsModule,
		ReactiveFormsModule,
		// Libraries
		NgbModule,
		// Application
		AppRoutingModule,
	],
	providers: [provideHttpClient()],
	bootstrap: [AppComponent],
})
export class AppModule {}

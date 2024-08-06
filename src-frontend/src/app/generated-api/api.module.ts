/* tslint:disable */
/* eslint-disable */
import {
	NgModule,
	ModuleWithProviders,
	SkipSelf,
	Optional,
} from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { ApiConfiguration, ApiConfigurationParams } from "./api-configuration";

import { PeopleService } from "./services/people.service";
import { TagsService } from "./services/tags.service";
import { ImagesService } from "./services/images.service";
import { AlbumsService } from "./services/albums.service";
import { PetsService } from "./services/pets.service";
import { LocationsService } from "./services/locations.service";
import { DatesService } from "./services/dates.service";

/**
 * Module that provides all services and configuration.
 */
@NgModule({
	imports: [],
	exports: [],
	declarations: [],
	providers: [
		PeopleService,
		TagsService,
		ImagesService,
		AlbumsService,
		PetsService,
		LocationsService,
		DatesService,
		ApiConfiguration,
	],
})
export class ApiModule {
	static forRoot(
		params: ApiConfigurationParams,
	): ModuleWithProviders<ApiModule> {
		return {
			ngModule: ApiModule,
			providers: [
				{
					provide: ApiConfiguration,
					useValue: params,
				},
			],
		};
	}

	constructor(
		@Optional() @SkipSelf() parentModule: ApiModule,
		@Optional() http: HttpClient,
	) {
		if (parentModule) {
			throw new Error(
				"ApiModule is already loaded. Import in your base AppModule only.",
			);
		}
		if (!http) {
			throw new Error(
				"You need to import the HttpClientModule in your AppModule! \n" +
					"See also https://github.com/angular/angular/issues/20575",
			);
		}
	}
}

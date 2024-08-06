/* tslint:disable */
/* eslint-disable */
import { Injectable } from "@angular/core";

/**
 * Global configuration
 */
@Injectable({
	providedIn: "root",
})
export class ApiConfiguration {
	// TODO: How to make configurable
	rootUrl: string = "http://localhost:8000/";
}

/**
 * Parameters for `ApiModule.forRoot()`
 */
export interface ApiConfigurationParams {
	rootUrl?: string;
}

/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { BaseService } from "../base-service";
import { ApiConfiguration } from "../api-configuration";
import { StrictHttpResponse } from "../strict-http-response";

import { createLocation } from "../fn/locations/create-location";
import { CreateLocation$Params } from "../fn/locations/create-location";
import { deleteLocation } from "../fn/locations/delete-location";
import { DeleteLocation$Params } from "../fn/locations/delete-location";
import { getLocation } from "../fn/locations/get-location";
import { GetLocation$Params } from "../fn/locations/get-location";
import { getLocations } from "../fn/locations/get-locations";
import { GetLocations$Params } from "../fn/locations/get-locations";
import { LocationReadSchema } from "../models/location-read-schema";
import { PagedLocationReadSchema } from "../models/paged-location-read-schema";
import { updateLocation } from "../fn/locations/update-location";
import { UpdateLocation$Params } from "../fn/locations/update-location";

@Injectable({ providedIn: "root" })
export class LocationsService extends BaseService {
	constructor(config: ApiConfiguration, http: HttpClient) {
		super(config, http);
	}

	/** Path part for operation `getLocations()` */
	static readonly GetLocationsPath = "/api/location/";

	/**
	 * Get All Locations.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getLocations()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getLocations$Response(
		params?: GetLocations$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PagedLocationReadSchema>> {
		return getLocations(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get All Locations.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getLocations$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getLocations(
		params?: GetLocations$Params,
		context?: HttpContext,
	): Observable<PagedLocationReadSchema> {
		return this.getLocations$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<PagedLocationReadSchema>,
				): PagedLocationReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `createLocation()` */
	static readonly CreateLocationPath = "/api/location/";

	/**
	 * Create Location.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `createLocation()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createLocation$Response(
		params: CreateLocation$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<LocationReadSchema>> {
		return createLocation(this.http, this.rootUrl, params, context);
	}

	/**
	 * Create Location.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `createLocation$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createLocation(
		params: CreateLocation$Params,
		context?: HttpContext,
	): Observable<LocationReadSchema> {
		return this.createLocation$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<LocationReadSchema>): LocationReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `getLocation()` */
	static readonly GetLocationPath = "/api/location/{location_id}/";

	/**
	 * Get Single Location.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getLocation()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getLocation$Response(
		params: GetLocation$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<LocationReadSchema>> {
		return getLocation(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Single Location.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getLocation$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getLocation(
		params: GetLocation$Params,
		context?: HttpContext,
	): Observable<LocationReadSchema> {
		return this.getLocation$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<LocationReadSchema>): LocationReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `deleteLocation()` */
	static readonly DeleteLocationPath = "/api/location/{location_id}/";

	/**
	 * Delete Location.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deleteLocation()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteLocation$Response(
		params: DeleteLocation$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<void>> {
		return deleteLocation(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Location.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deleteLocation$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteLocation(
		params: DeleteLocation$Params,
		context?: HttpContext,
	): Observable<void> {
		return this.deleteLocation$Response(params, context).pipe(
			map((r: StrictHttpResponse<void>): void => r.body),
		);
	}

	/** Path part for operation `updateLocation()` */
	static readonly UpdateLocationPath = "/api/location/{location_id}/";

	/**
	 * Update Location.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updateLocation()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateLocation$Response(
		params: UpdateLocation$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<LocationReadSchema>> {
		return updateLocation(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Location.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updateLocation$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateLocation(
		params: UpdateLocation$Params,
		context?: HttpContext,
	): Observable<LocationReadSchema> {
		return this.updateLocation$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<LocationReadSchema>): LocationReadSchema =>
					r.body,
			),
		);
	}
}

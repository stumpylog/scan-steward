/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { BaseService } from "../base-service";
import { ApiConfiguration } from "../api-configuration";
import { StrictHttpResponse } from "../strict-http-response";

import { createRoughDate } from "../fn/dates/create-rough-date";
import { CreateRoughDate$Params } from "../fn/dates/create-rough-date";
import { deleteRoughDate } from "../fn/dates/delete-rough-date";
import { DeleteRoughDate$Params } from "../fn/dates/delete-rough-date";
import { getRoughDates } from "../fn/dates/get-rough-dates";
import { GetRoughDates$Params } from "../fn/dates/get-rough-dates";
import { getSingleRoughDate } from "../fn/dates/get-single-rough-date";
import { GetSingleRoughDate$Params } from "../fn/dates/get-single-rough-date";
import { PagedRoughDateReadSchema } from "../models/paged-rough-date-read-schema";
import { RoughDateReadSchema } from "../models/rough-date-read-schema";
import { updateRoughDate } from "../fn/dates/update-rough-date";
import { UpdateRoughDate$Params } from "../fn/dates/update-rough-date";

@Injectable({ providedIn: "root" })
export class DatesService extends BaseService {
	constructor(config: ApiConfiguration, http: HttpClient) {
		super(config, http);
	}

	/** Path part for operation `getRoughDates()` */
	static readonly GetRoughDatesPath = "/api/date/";

	/**
	 * Get All Dates.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getRoughDates()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getRoughDates$Response(
		params?: GetRoughDates$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PagedRoughDateReadSchema>> {
		return getRoughDates(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get All Dates.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getRoughDates$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getRoughDates(
		params?: GetRoughDates$Params,
		context?: HttpContext,
	): Observable<PagedRoughDateReadSchema> {
		return this.getRoughDates$Response(params, context).pipe(
			map(
				(
					r: StrictHttpResponse<PagedRoughDateReadSchema>,
				): PagedRoughDateReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `createRoughDate()` */
	static readonly CreateRoughDatePath = "/api/date/";

	/**
	 * Create Rough Date.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `createRoughDate()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createRoughDate$Response(
		params: CreateRoughDate$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<RoughDateReadSchema>> {
		return createRoughDate(this.http, this.rootUrl, params, context);
	}

	/**
	 * Create Rough Date.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `createRoughDate$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createRoughDate(
		params: CreateRoughDate$Params,
		context?: HttpContext,
	): Observable<RoughDateReadSchema> {
		return this.createRoughDate$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<RoughDateReadSchema>): RoughDateReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `getSingleRoughDate()` */
	static readonly GetSingleRoughDatePath = "/api/date/{date_id}/";

	/**
	 * Get Single Rough Date.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getSingleRoughDate()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSingleRoughDate$Response(
		params: GetSingleRoughDate$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<RoughDateReadSchema>> {
		return getSingleRoughDate(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Single Rough Date.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getSingleRoughDate$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSingleRoughDate(
		params: GetSingleRoughDate$Params,
		context?: HttpContext,
	): Observable<RoughDateReadSchema> {
		return this.getSingleRoughDate$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<RoughDateReadSchema>): RoughDateReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `deleteRoughDate()` */
	static readonly DeleteRoughDatePath = "/api/date/{date_id}/";

	/**
	 * Delete Rough Date.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deleteRoughDate()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteRoughDate$Response(
		params: DeleteRoughDate$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<void>> {
		return deleteRoughDate(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Rough Date.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deleteRoughDate$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deleteRoughDate(
		params: DeleteRoughDate$Params,
		context?: HttpContext,
	): Observable<void> {
		return this.deleteRoughDate$Response(params, context).pipe(
			map((r: StrictHttpResponse<void>): void => r.body),
		);
	}

	/** Path part for operation `updateRoughDate()` */
	static readonly UpdateRoughDatePath = "/api/date/{date_id}/";

	/**
	 * Update Rough Date.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updateRoughDate()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateRoughDate$Response(
		params: UpdateRoughDate$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<RoughDateReadSchema>> {
		return updateRoughDate(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Rough Date.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updateRoughDate$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updateRoughDate(
		params: UpdateRoughDate$Params,
		context?: HttpContext,
	): Observable<RoughDateReadSchema> {
		return this.updateRoughDate$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<RoughDateReadSchema>): RoughDateReadSchema =>
					r.body,
			),
		);
	}
}

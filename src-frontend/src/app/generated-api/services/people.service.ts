/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { BaseService } from "../base-service";
import { ApiConfiguration } from "../api-configuration";
import { StrictHttpResponse } from "../strict-http-response";

import { createPerson } from "../fn/people/create-person";
import { CreatePerson$Params } from "../fn/people/create-person";
import { deletePerson } from "../fn/people/delete-person";
import { DeletePerson$Params } from "../fn/people/delete-person";
import { getPeople } from "../fn/people/get-people";
import { GetPeople$Params } from "../fn/people/get-people";
import { getPerson } from "../fn/people/get-person";
import { GetPerson$Params } from "../fn/people/get-person";
import { PagedPersonReadSchema } from "../models/paged-person-read-schema";
import { PersonReadSchema } from "../models/person-read-schema";
import { updatePerson } from "../fn/people/update-person";
import { UpdatePerson$Params } from "../fn/people/update-person";

@Injectable({ providedIn: "root" })
export class PeopleService extends BaseService {
	constructor(config: ApiConfiguration, http: HttpClient) {
		super(config, http);
	}

	/** Path part for operation `getPeople()` */
	static readonly GetPeoplePath = "/api/person/";

	/**
	 * Get All People.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getPeople()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPeople$Response(
		params?: GetPeople$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PagedPersonReadSchema>> {
		return getPeople(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get All People.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getPeople$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPeople(
		params?: GetPeople$Params,
		context?: HttpContext,
	): Observable<PagedPersonReadSchema> {
		return this.getPeople$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<PagedPersonReadSchema>): PagedPersonReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `createPerson()` */
	static readonly CreatePersonPath = "/api/person/";

	/**
	 * Create Person.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `createPerson()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createPerson$Response(
		params: CreatePerson$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PersonReadSchema>> {
		return createPerson(this.http, this.rootUrl, params, context);
	}

	/**
	 * Create Person.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `createPerson$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createPerson(
		params: CreatePerson$Params,
		context?: HttpContext,
	): Observable<PersonReadSchema> {
		return this.createPerson$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<PersonReadSchema>): PersonReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `getPerson()` */
	static readonly GetPersonPath = "/api/person/{person_id}/";

	/**
	 * Get Single Person.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getPerson()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPerson$Response(
		params: GetPerson$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PersonReadSchema>> {
		return getPerson(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Single Person.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getPerson$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPerson(
		params: GetPerson$Params,
		context?: HttpContext,
	): Observable<PersonReadSchema> {
		return this.getPerson$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<PersonReadSchema>): PersonReadSchema => r.body,
			),
		);
	}

	/** Path part for operation `deletePerson()` */
	static readonly DeletePersonPath = "/api/person/{person_id}/";

	/**
	 * Delete Person.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deletePerson()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deletePerson$Response(
		params: DeletePerson$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<void>> {
		return deletePerson(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Person.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deletePerson$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deletePerson(
		params: DeletePerson$Params,
		context?: HttpContext,
	): Observable<void> {
		return this.deletePerson$Response(params, context).pipe(
			map((r: StrictHttpResponse<void>): void => r.body),
		);
	}

	/** Path part for operation `updatePerson()` */
	static readonly UpdatePersonPath = "/api/person/{person_id}/";

	/**
	 * Update Person.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updatePerson()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updatePerson$Response(
		params: UpdatePerson$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PersonReadSchema>> {
		return updatePerson(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Person.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updatePerson$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updatePerson(
		params: UpdatePerson$Params,
		context?: HttpContext,
	): Observable<PersonReadSchema> {
		return this.updatePerson$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<PersonReadSchema>): PersonReadSchema => r.body,
			),
		);
	}
}

/* tslint:disable */
/* eslint-disable */
import { HttpClient, HttpContext } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { BaseService } from "../base-service";
import { ApiConfiguration } from "../api-configuration";
import { StrictHttpResponse } from "../strict-http-response";

import { createPet } from "../fn/pets/create-pet";
import { CreatePet$Params } from "../fn/pets/create-pet";
import { deletePet } from "../fn/pets/delete-pet";
import { DeletePet$Params } from "../fn/pets/delete-pet";
import { getPets } from "../fn/pets/get-pets";
import { GetPets$Params } from "../fn/pets/get-pets";
import { getSinglePet } from "../fn/pets/get-single-pet";
import { GetSinglePet$Params } from "../fn/pets/get-single-pet";
import { PagedPetReadSchema } from "../models/paged-pet-read-schema";
import { PetReadSchema } from "../models/pet-read-schema";
import { updatePet } from "../fn/pets/update-pet";
import { UpdatePet$Params } from "../fn/pets/update-pet";

@Injectable({ providedIn: "root" })
export class PetsService extends BaseService {
	constructor(config: ApiConfiguration, http: HttpClient) {
		super(config, http);
	}

	/** Path part for operation `getPets()` */
	static readonly GetPetsPath = "/api/pet/";

	/**
	 * Get All Pets.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getPets()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPets$Response(
		params?: GetPets$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PagedPetReadSchema>> {
		return getPets(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get All Pets.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getPets$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getPets(
		params?: GetPets$Params,
		context?: HttpContext,
	): Observable<PagedPetReadSchema> {
		return this.getPets$Response(params, context).pipe(
			map(
				(r: StrictHttpResponse<PagedPetReadSchema>): PagedPetReadSchema =>
					r.body,
			),
		);
	}

	/** Path part for operation `createPet()` */
	static readonly CreatePetPath = "/api/pet/";

	/**
	 * Create Pet.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `createPet()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createPet$Response(
		params: CreatePet$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PetReadSchema>> {
		return createPet(this.http, this.rootUrl, params, context);
	}

	/**
	 * Create Pet.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `createPet$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	createPet(
		params: CreatePet$Params,
		context?: HttpContext,
	): Observable<PetReadSchema> {
		return this.createPet$Response(params, context).pipe(
			map((r: StrictHttpResponse<PetReadSchema>): PetReadSchema => r.body),
		);
	}

	/** Path part for operation `getSinglePet()` */
	static readonly GetSinglePetPath = "/api/pet/{pet_id}/";

	/**
	 * Get Single Pet.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `getSinglePet()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSinglePet$Response(
		params: GetSinglePet$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PetReadSchema>> {
		return getSinglePet(this.http, this.rootUrl, params, context);
	}

	/**
	 * Get Single Pet.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `getSinglePet$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	getSinglePet(
		params: GetSinglePet$Params,
		context?: HttpContext,
	): Observable<PetReadSchema> {
		return this.getSinglePet$Response(params, context).pipe(
			map((r: StrictHttpResponse<PetReadSchema>): PetReadSchema => r.body),
		);
	}

	/** Path part for operation `deletePet()` */
	static readonly DeletePetPath = "/api/pet/{pet_id}/";

	/**
	 * Delete Pet.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `deletePet()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deletePet$Response(
		params: DeletePet$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<void>> {
		return deletePet(this.http, this.rootUrl, params, context);
	}

	/**
	 * Delete Pet.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `deletePet$Response()` instead.
	 *
	 * This method doesn't expect any request body.
	 */
	deletePet(params: DeletePet$Params, context?: HttpContext): Observable<void> {
		return this.deletePet$Response(params, context).pipe(
			map((r: StrictHttpResponse<void>): void => r.body),
		);
	}

	/** Path part for operation `updatePet()` */
	static readonly UpdatePetPath = "/api/pet/{pet_id}/";

	/**
	 * Update Pet.
	 *
	 *
	 *
	 * This method provides access to the full `HttpResponse`, allowing access to response headers.
	 * To access only the response body, use `updatePet()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updatePet$Response(
		params: UpdatePet$Params,
		context?: HttpContext,
	): Observable<StrictHttpResponse<PetReadSchema>> {
		return updatePet(this.http, this.rootUrl, params, context);
	}

	/**
	 * Update Pet.
	 *
	 *
	 *
	 * This method provides access only to the response body.
	 * To access the full response (for headers, for example), `updatePet$Response()` instead.
	 *
	 * This method sends `application/json` and handles request body of type `application/json`.
	 */
	updatePet(
		params: UpdatePet$Params,
		context?: HttpContext,
	): Observable<PetReadSchema> {
		return this.updatePet$Response(params, context).pipe(
			map((r: StrictHttpResponse<PetReadSchema>): PetReadSchema => r.body),
		);
	}
}
